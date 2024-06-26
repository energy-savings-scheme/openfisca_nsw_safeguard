from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class HVAC1_PDRSAug24_baseline_input_power(Variable):
    ''' Note that baseline input power is the same value as input power
    '''
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Baseline input'

    def formula(buildings, period, parameters):
      rated_cooling_capacity = buildings('HVAC1_PDRSAug24_cooling_capacity_input', period)
      baseline_AEER = buildings('HVAC1_PDRSAug24_baseline_AEER_input', period)
      
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


class HVAC1_PDRSAug24_BCA_climate_zone_by_postcode(Variable):
    #this determines the expected BCA Climate Zone
    value_type = str
    entity = Building
    definition_period = ETERNITY
    metadata={
        'variable-type': 'inter-interesting',
    }

    def formula(buildings, period, parameters):
        postcode = buildings('HVAC1_PDRSAug24_PDRS__postcode', period)
        # Returns an integer
        climate_zone = parameters(period).ESS.ESS_general.table_A26_BCA_climate_zone_by_postcode       
        climate_zone_int = climate_zone.calc(postcode)
        return climate_zone_int


class HVAC1_PDRSAug24_BCAClimateZone(Enum):
     BCA_Climate_Zone_1 = 'BCA Climate Zone 1',
     BCA_Climate_Zone_2 = 'BCA Climate Zone 2',
     BCA_Climate_Zone_3 = 'BCA Climate Zone 3',
     BCA_Climate_Zone_4 = 'BCA Climate Zone 4',
     BCA_Climate_Zone_5 = 'BCA Climate Zone 5',
     BCA_Climate_Zone_6 = 'BCA Climate Zone 6',
     BCA_Climate_Zone_7 = 'BCA Climate Zone 7',
     BCA_Climate_Zone_8 = 'BCA Climate Zone 8'


class HVAC1_PDRSAug24_BCA_Climate_Zone(Variable):
    #this is where the user can change their BCA Climate Zone manually
    value_type = Enum
    entity = Building
    default_value = HVAC1_PDRSAug24_BCAClimateZone.BCA_Climate_Zone_5 #this should equal HVAC1_PDRSAug24_BCA_climate_zone_by_postcode
    possible_values = HVAC1_PDRSAug24_BCAClimateZone
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'BCA Climate Zone',
        'display_question' : 'Certain postcodes can belong to multiple climate zones, check your BCA Climate Zone on the map.',
        'sorting' : 2
    }


class HVAC1_PDRSAug24_baseline_peak_adjustment_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HVAC1 baseline peak adjustment factor'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
      usage_factor = 0.72
      climate_zone = buildings('HVAC1_PDRSAug24_BCA_Climate_Zone', period)
      temp_factor = parameters(period).PDRS.table_A28_temperature_factor.temperature_factor[climate_zone]

      baseline_adjustment_factor = usage_factor * temp_factor
      return baseline_adjustment_factor


class HVAC1_PDRSAug24_peak_demand_savings_activity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand savings activity'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        baseline_input_power = buildings('HVAC1_PDRSAug24_baseline_input_power', period)
        baseline_peak_adjustment = buildings('HVAC1_PDRSAug24_baseline_peak_adjustment_factor', period)
        input_power = buildings('HVAC1_PDRSAug24_input_power', period)
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


class HVAC1_PDRSAug24_peak_demand_annual_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand annual savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #baseline input power
        rated_cooling_capacity = buildings('HVAC1_PDRSAug24_cooling_capacity_input', period)
        baseline_AEER = buildings('HVAC1_PDRSAug24_baseline_AEER_input', period)
      
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
        climate_zone = buildings('HVAC1_PDRSAug24_BCA_Climate_Zone', period)
        temp_factor = parameters(period).PDRS.table_A28_temperature_factor.temperature_factor[climate_zone]

        baseline_peak_adjustment = usage_factor * temp_factor

        #peak demand savings activity
        input_power = buildings('HVAC1_PDRSAug24_input_power', period)
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
        peak_demand_annual_savings_return = np.select([
                peak_demand_annual_savings <= 0, peak_demand_annual_savings > 0
            ], 
	        [
                0, peak_demand_annual_savings
            ])
        
        return peak_demand_annual_savings_return
    

class HVAC1_PDRSAug24_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand reduction capacity'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        peak_demand_savings = buildings('HVAC1_PDRSAug24_peak_demand_savings_activity', period)
        summer_peak_demand_duration = 6
        lifetime = 10

        peak_demand_reduction_capacity = (peak_demand_savings * summer_peak_demand_duration * lifetime)
        return peak_demand_reduction_capacity


class HVAC1_PDRSAug24_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of PRCs for HVAC1'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        peak_demand_capacity = buildings('HVAC1_PDRSAug24_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('HVAC1_PDRSAug24_get_network_loss_factor_by_postcode', period)
        kw_to_0_1kw = 10
        
        HVAC1_PDRSAug24_TCSPF_or_AEER_exceeds_ESS_benchmark = buildings('HVAC1_PDRSAug24_TCSPF_or_AEER_exceeds_ESS_benchmark', period)

        result = np.floor(peak_demand_capacity * network_loss_factor * kw_to_0_1kw)
        result_meet_elig = np.select(
                        [
                         HVAC1_PDRSAug24_TCSPF_or_AEER_exceeds_ESS_benchmark,
                         np.logical_not(HVAC1_PDRSAug24_TCSPF_or_AEER_exceeds_ESS_benchmark)
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
    

class HVAC1_PDRSAug24_PRC_savings_check(Variable):
    #this variable checks if PRCs are zero, and if they are returns zero peak savings
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        number_of_prcs = buildings('HVAC1_PDRSAug24_PRC_calculation', period)
        peak_demand_annual_savings = buildings('HVAC1_PDRSAug24_peak_demand_annual_savings', period)
        
        peak_demand_annual_savings_check = np.select([
                number_of_prcs <= 0,
                number_of_prcs > 0
            ],
            [
                0,
                peak_demand_annual_savings
            ])

        return peak_demand_annual_savings_check