from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class RF1_number_of_refrigerator_freezers_removal(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    metadata = {
        'label' : 'Number of refrigerator or freezers removed',
        'display_question' : 'How many non-primary refrigerators or freezers are you removing?',
        'sorting' : 3
    }


class RF1_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
      number_fridges_freezers = buildings('RF1_number_of_refrigerator_freezers_removal', period)

      deemed_electricity_savings = number_fridges_freezers * 5.7
      return deemed_electricity_savings


class RF1_PDRS__regional_network_factor(Variable):
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
        postcode = buildings('RF1_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode) 


class RF1_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'RF2 Electricity savings'
    metadata = {
        'alias': 'RF2 electricity savings',
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('RF1_deemed_activity_electricity_savings', period)   
        regional_network_factor = buildings('RF1_PDRS__regional_network_factor', period)

        RF2_electricity_savings = deemed_electricity_savings * regional_network_factor
        return RF2_electricity_savings


class RF1_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for HVAC1'

    def formula(buildings, period, parameters):
        RF1_electricity_savings = buildings('RF1_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        storage_volume_eligibility = buildings('RF1_storage_volume', period)

        RF1_eligible_ESCs = np.select(
        [
            storage_volume_eligibility,
            np.logical_not(storage_volume_eligibility)
        ],
        [
            (RF1_electricity_savings * electricity_certificate_conversion_factor),
            0
        ])

        result_to_return = np.select(
            [
                RF1_eligible_ESCs <= 0, RF1_eligible_ESCs > 0
            ],
            [
                0, RF1_eligible_ESCs
            ])
        return result_to_return