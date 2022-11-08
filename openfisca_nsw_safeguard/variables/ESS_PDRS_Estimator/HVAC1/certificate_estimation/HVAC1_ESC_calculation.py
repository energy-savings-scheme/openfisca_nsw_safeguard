from email.mime import base
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

np.set_printoptions(suppress=True)


class HVAC1_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual heating energy use'
    metadata = {
        "alias": "Annual heating energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      heating_capacity = buildings('HVAC1_heating_capacity_input', period)
      equivalent_heating_hours = buildings('HVAC1_equivalent_heating_hours_input', period)
      rated_ACOP = buildings('HVAC1_rated_ACOP_input', period)
      
      return np.select([    
                            rated_ACOP == 0,
                            (heating_capacity * equivalent_heating_hours) > 0, 
                            (heating_capacity * equivalent_heating_hours) == 0,
                            (heating_capacity * equivalent_heating_hours) < 0
                        ],
                        [
                            0,
                            (heating_capacity * equivalent_heating_hours) / rated_ACOP, 
                            0,
                            (heating_capacity * equivalent_heating_hours) / rated_ACOP
                        ])

class HVAC1_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual cooling energy use'
    metadata = {
        "alias": "Annual cooling energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      cooling_capacity = buildings('HVAC1_cooling_capacity_input', period)
      equivalent_cooling_hours = buildings('HVAC1_equivalent_cooling_hours_input', period)
      rated_AEER = buildings('HVAC1_rated_AEER_input', period)
      
      return np.select([    
                    rated_AEER == 0,
                    (cooling_capacity * equivalent_cooling_hours) > 0, 
                    (cooling_capacity * equivalent_cooling_hours) == 0,
                    (cooling_capacity * equivalent_cooling_hours) < 0
                ],
                [
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / rated_AEER, 
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / rated_AEER
                ])


class HVAC1_reference_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Reference annual heating energy use'
    metadata = {
        "alias": "Reference annual heating energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      heating_capacity = buildings('HVAC1_heating_capacity_input', period)
      equivalent_heating_hours = buildings('HVAC1_equivalent_heating_hours_input', period)
      baseline_ACOP = buildings('HVAC1_baseline_ACOP_input', period)
      
      
      return np.select([    
                        baseline_ACOP == 0,
                        (heating_capacity * equivalent_heating_hours) > 0, 
                        (heating_capacity * equivalent_heating_hours) == 0,
                        (heating_capacity * equivalent_heating_hours) < 0
                    ],
                    [
                        0,
                        (heating_capacity * equivalent_heating_hours) / baseline_ACOP, 
                        0,
                        (heating_capacity * equivalent_heating_hours) / baseline_ACOP
                    ])

  
class HVAC1_reference_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Reference annual cooling energy use'
    metadata = {
        "alias": "Reference annual cooling energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      cooling_capacity = buildings('HVAC1_cooling_capacity_input', period)
      equivalent_cooling_hours = buildings('HVAC1_equivalent_cooling_hours_input', period)
      baseline_AEER = buildings('HVAC1_baseline_AEER_input', period)
      
      return np.select([  
                    baseline_AEER == 0,  
                    (cooling_capacity * equivalent_cooling_hours) > 0, 
                    (cooling_capacity * equivalent_cooling_hours) == 0,
                    (cooling_capacity * equivalent_cooling_hours) < 0
                ],
                [
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / baseline_AEER, 
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / baseline_AEER
                ])


class HVAC1_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "alias": "Deemed activity electricity savings",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      reference_annual_cooling = buildings('HVAC1_reference_cooling_annual_energy_use', period)
      annual_cooling = buildings('HVAC1_cooling_annual_energy_use', period)
      reference_annual_heating = buildings('HVAC1_reference_heating_annual_energy_use', period)
      annual_heating = buildings('HVAC1_heating_annual_energy_use', period)
      lifetime = 10
      
      deemed_electricity_savings = np.multiply(((reference_annual_cooling - annual_cooling) + (reference_annual_heating - annual_heating)), (lifetime / 1000))
      return deemed_electricity_savings


class HVAC1_PDRS__regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'
    metadata = {
        "variable-type": "inter-interesting",
        "alias":"PDRS Regional Network Factor",
        "display_question": "PDRS regional network factor",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        postcode = buildings('HVAC1_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided


class HVAC1_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HVAC1 Electricity savings'
    metadata = {
        "alias": "HVAC1 electricity savings",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('HVAC1_deemed_activity_electricity_savings', period)  # 2798.25 
        regional_network_factor = buildings('HVAC1_PDRS__regional_network_factor', period)

        HVAC1_electricity_savings = (deemed_electricity_savings * regional_network_factor)
        return HVAC1_electricity_savings


class HVAC1_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for HVAC1'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      HVAC1_electricity_savings = buildings('HVAC1_electricity_savings', period)
      electricity_certificate_conversion_factor = 1.06

      result = HVAC1_electricity_savings * electricity_certificate_conversion_factor
      result_to_return = np.select([
                result < 0, result > 0
            ], [
                0, result
            ])

      return result_to_return
