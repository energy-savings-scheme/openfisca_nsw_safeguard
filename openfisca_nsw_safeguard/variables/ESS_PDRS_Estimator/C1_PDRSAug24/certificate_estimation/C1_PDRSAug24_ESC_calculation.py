from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class C1_PDRSAug24_number_of_refrigerator_freezers_removal(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    metadata = {
        'label' : 'Number of refrigerator or freezers removed',
        'display_question' : 'How many non-primary refrigerators or freezers are you removing?',
        'sorting' : 3
    }


class C1_PDRSAug24_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
      number_fridges_freezers = buildings('C1_PDRSAug24_number_of_refrigerator_freezers_removal', period)

      deemed_electricity_savings = number_fridges_freezers * 5.7
      return deemed_electricity_savings


class C1_PDRSAug24_energy_savings(Variable):
    value_type = float  
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
      number_fridges_freezers = buildings('C1_PDRSAug24_number_of_refrigerator_freezers_removal', period)

      #deemed electricity savings
      deemed_electricity_savings = number_fridges_freezers * 5.7
      
      #regional network factor
      postcode = buildings('C1_PDRSAug24_PDRS__postcode', period)
      rnf = parameters(period).PDRS.table_A24_regional_network_factor
      regional_network_factor = rnf.calc(postcode) 
   
      #electricity savings
      annual_energy_savings = deemed_electricity_savings * regional_network_factor

      annual_savings_return = np.select([
            annual_energy_savings <= 0, annual_energy_savings > 0
        ], 
	    [
            0, annual_energy_savings
        ])
        
      return annual_savings_return


class C1_PDRSAug24_PDRS__regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'
    metadata = {
        'variable-type': 'inter-interesting',
        'alias':'PDRS Regional Network Factor',
        'display_question': 'PDRS regional network factor'
    }

    def formula(buildings, period, parameters):
        postcode = buildings('C1_PDRSAug24_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode) 


class C1_PDRSAug24_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'RF2 Electricity savings'
    metadata = {
        'alias': 'RF2 electricity savings',
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('C1_PDRSAug24_deemed_activity_electricity_savings', period)   
        regional_network_factor = buildings('C1_PDRSAug24_PDRS__regional_network_factor', period)

        RF2_electricity_savings = deemed_electricity_savings * regional_network_factor
        return RF2_electricity_savings


class C1_PDRSAug24_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for HVAC1'

    def formula(buildings, period, parameters):
        C1_PDRSAug24_electricity_savings = buildings('C1_PDRSAug24_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        storage_volume_eligibility = buildings('C1_PDRSAug24_storage_volume', period)

        C1_PDRSAug24_eligible_ESCs = np.select(
            [
                storage_volume_eligibility,
                np.logical_not(storage_volume_eligibility)
            ],
            [
                (C1_PDRSAug24_electricity_savings * electricity_certificate_conversion_factor),
                0
            ])

        result_to_return = np.select(
            [
                C1_PDRSAug24_eligible_ESCs <= 0, 
                C1_PDRSAug24_eligible_ESCs > 0
            ],
            [
                0, 
                C1_PDRSAug24_eligible_ESCs
            ])
        return result_to_return