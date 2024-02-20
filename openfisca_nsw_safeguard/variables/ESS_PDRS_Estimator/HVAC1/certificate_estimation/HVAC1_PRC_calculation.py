from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class HVAC1_baseline_input_power(Variable):
    """ Note that baseline input power is the same value as input power
    """
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Baseline input'

    def formula(buildings, period, parameters):
      rated_cooling_capacity = buildings('HVAC1_cooling_capacity_input', period)
      baseline_AEER = buildings('HVAC1_baseline_AEER_input', period)
      
      return np.select([    
                    baseline_AEER == 0,
                    (rated_cooling_capacity / baseline_AEER) > 0, 
                    (rated_cooling_capacity / baseline_AEER) == 0,
                    (rated_cooling_capacity / baseline_AEER) < 0
                ],
                [
                    0,
                    rated_cooling_capacity / baseline_AEER,
                    0,
                    rated_cooling_capacity / baseline_AEER
                ])


class HVAC1_BCA_climate_zone_by_postcode(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'What BCA climate zone is the activity taking place in?'
    metadata={
        "variable-type": "inter-interesting",
        "alias": "HVAC1 BCA Climate Zone",
    }

    def formula(buildings, period, parameters):
        postcode = buildings('HVAC1_PDRS__postcode', period)
        # Returns an integer
        climate_zone = parameters(period).ESS.ESS_general.table_A26_BCA_climate_zone_by_postcode       
        climate_zone_int = climate_zone.calc(postcode)
        cooling_capacity_to_check = np.select(
            [
                climate_zone_int == 1,
                climate_zone_int == 2,
                climate_zone_int == 3,
                climate_zone_int == 4,
                climate_zone_int == 5,
                climate_zone_int == 6,
                climate_zone_int == 7,
                climate_zone_int == 8
            ],
            [
                "BCA_Climate_Zone_1",
                "BCA_Climate_Zone_2",
                "BCA_Climate_Zone_3",
                "BCA_Climate_Zone_4",
                "BCA_Climate_Zone_5",
                "BCA_Climate_Zone_6",
                "BCA_Climate_Zone_7",
                "BCA_Climate_Zone_8"
            ])

        return cooling_capacity_to_check


class HVAC1_baseline_peak_adjustment_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HVAC1 baseline peak adjustment factor'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      usage_factor = 0.72
      climate_zone = buildings('HVAC1_BCA_climate_zone_by_postcode', period)
      temp_factor = parameters(period).PDRS.table_A28_temperature_factor.temperature_factor[climate_zone]

      baseline_adjustment_factor = usage_factor * temp_factor
      return baseline_adjustment_factor


class HVAC1_peak_demand_savings_activity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand savings activity'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        baseline_input_power = buildings('HVAC1_baseline_input_power', period)
        baseline_peak_adjustment = buildings('HVAC1_baseline_peak_adjustment_factor', period)
        input_power = buildings('HVAC1_input_power', period)
        firmness_factor = 1

        return (
                    (
                        baseline_input_power *
                        baseline_peak_adjustment
                    ) -
                    (
                        input_power *
                        baseline_peak_adjustment
                    )
                    *
                    firmness_factor
            )


class HVAC1_peak_demand_annual_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand annual savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        #baseline input power
        rated_cooling_capacity = buildings('HVAC1_cooling_capacity_input', period)
        baseline_AEER = buildings('HVAC1_baseline_AEER_input', period)
      
        baseline_input_power = np.select([    
                    baseline_AEER == 0,
                    (rated_cooling_capacity / baseline_AEER) > 0, 
                    (rated_cooling_capacity / baseline_AEER) == 0,
                    (rated_cooling_capacity / baseline_AEER) < 0
                ],
                [
                    0,
                    rated_cooling_capacity / baseline_AEER,
                    0,
                    rated_cooling_capacity / baseline_AEER
                ])

        #baseline peak adjustment factor
        usage_factor = 0.72
        climate_zone = buildings('HVAC1_BCA_climate_zone_by_postcode', period)
        temp_factor = parameters(period).PDRS.table_A28_temperature_factor.temperature_factor[climate_zone]

        baseline_peak_adjustment = usage_factor * temp_factor

        #peak demand savings activity
        input_power = buildings('HVAC1_input_power', period)
        firmness_factor = 1

        peak_demand_savings_activity = (
                    (
                        baseline_input_power *
                        baseline_peak_adjustment
                    ) -
                    (
                        input_power *
                        baseline_peak_adjustment
                    )
                    *
                    firmness_factor
            )

        #peak demand reduction capacity
        summer_peak_demand_duration = 6
        lifetime = 10

        peak_demand_annual_savings = (peak_demand_savings_activity * summer_peak_demand_duration * lifetime)
        return peak_demand_annual_savings
    

class HVAC1_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand reduction capacity'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        peak_demand_savings = buildings('HVAC1_peak_demand_savings_activity', period)
        summer_peak_demand_duration = 6
        lifetime = 10

        peak_demand_reduction_capacity = (peak_demand_savings * summer_peak_demand_duration * lifetime)
        return peak_demand_reduction_capacity


class HVAC1_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of PRCs for HVAC1'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        peak_demand_capacity = buildings('HVAC1_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('HVAC1_get_network_loss_factor_by_postcode', period)
        kw_to_0_1kw = 10
        
        
        HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark = buildings('HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark', period)

        result = np.floor(peak_demand_capacity * network_loss_factor * kw_to_0_1kw)
        result_meet_elig = np.select(
                        [
                         HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark,
                         np.logical_not(HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark)
                         ],
                        [
                            result, 0
                        ])

        result_to_return = np.select([
                result_meet_elig <= 0, result_meet_elig > 0
            ], [
                0, result_meet_elig
            ])
        return result_to_return
    

class HVAC1_PRC_savings_check(Variable):
    #this variable checks if PRCs are zero, and if they are returns zero peak savings
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        number_of_prcs = buildings('HVAC1_PRC_calculation', period)
        peak_demand_annual_savings = buildings('HVAC1_peak_demand_annual_savings', period)
        
        peak_demand_annual_savings_check = np.select([
                number_of_prcs <= 0,
                number_of_prcs > 0
            ],
            [
                0,
                peak_demand_annual_savings
            ])

        return peak_demand_annual_savings_check
