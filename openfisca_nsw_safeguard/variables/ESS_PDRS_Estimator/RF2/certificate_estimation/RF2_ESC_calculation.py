from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class RF2_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      total_energy_consumption = buildings('RF2_total_energy_consumption', period)
      af = buildings('RF2_af', period)

      input_power = (total_energy_consumption * af) / 24
      return input_power


class RF2_lifetime_by_rc_class(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
 
    def formula(buildings, period, parameters):
        product_class = buildings("RF2_product_class_int", period) # 3
        display_area =  buildings('RF2_total_display_area', period)
        
        lifetime_by_rc_class = np.select(
            [
                (product_class == 1),
                (product_class == 2),
                (product_class == 3),
                (product_class == 4),
                (product_class == 5),
                (product_class == 6),
                (product_class == 9),
                (product_class == 10),
                np.logical_and(product_class == 7, display_area < 3.3),
                np.logical_and(product_class == 8 , display_area < 3.3),
                np.logical_and(product_class == 11, display_area < 3.3),
                np.logical_and(product_class == 7, display_area >= 3.3),
                np.logical_and(product_class == 8, display_area >= 3.3),
                np.logical_and(product_class == 11, display_area >= 3.3),
                (product_class >= 12) * (product_class <= 15),
            ],
            [
                8,
                8,
                8,
                8,
                8,
                8,
                8,
                8,
                8,
                8,
                8,
                12,
                12,
                12,
                12,
            
            ])

        return lifetime_by_rc_class


class RF2_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
      total_energy_consumption = buildings('RF2_total_energy_consumption', period)
      baseline_EEI = buildings('RF2_baseline_EEI', period)
      product_EEI = buildings('RF2_product_EEI', period)
      af = buildings('RF2_af', period)
      lifetime_by_rc_class = buildings('RF2_lifetime_by_rc_class', period)

      deemed_electricity_savings = np.multiply(total_energy_consumption * (baseline_EEI / product_EEI - 1) * af * 365, (lifetime_by_rc_class / 1000))
      return deemed_electricity_savings


class RF2_PDRS__regional_network_factor(Variable):
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
        postcode = buildings('RF2_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode) 


class RF2_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'RF2 Electricity savings'
    metadata = {
        'alias': 'RF2 electricity savings',
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('RF2_deemed_activity_electricity_savings', period)   
        regional_network_factor = buildings('RF2_PDRS__regional_network_factor', period)

        RF2_electricity_savings = deemed_electricity_savings * regional_network_factor
        return RF2_electricity_savings
  

class RF2_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for HVAC1'

    def formula(buildings, period, parameters):
      RF2_electricity_savings = buildings('RF2_electricity_savings', period)
      electricity_certificate_conversion_factor = 1.06

      result = RF2_electricity_savings * electricity_certificate_conversion_factor
      result_to_return = np.select([
                result <= 0, result > 0 
            ], [
                0, result
            ])

      return result_to_return
