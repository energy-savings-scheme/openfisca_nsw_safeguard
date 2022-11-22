from xml.etree import ElementInclude
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class SYS1_baseline_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Baseline input power (kW)'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        # user input
        SYS1_new_equipment_rated_output = buildings('SYS1_new_equipment_rated_output', period)
        SYS1_baseline_efficiency = buildings('SYS1_new_equipment_baseline_efficiency', period)

        baseline_input_power = SYS1_new_equipment_rated_output * (SYS1_baseline_efficiency/100)
        return baseline_input_power
    
    
class SYS1_baseline_peak_adjustment_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        # user input
        climate_zone = buildings('SYS1_BCA_climate_zone_by_postcode', period)
        temp_factor = parameters(period).PDRS.table_A28_temperature_factor.temperature_factor[climate_zone]
        # temp_factor = buildings('SYS1_temperature_factor', period)
        usage_factor = 0.6

        baseline_peak_adjustment_factor = temp_factor * usage_factor
        return baseline_peak_adjustment_factor


class SYS1_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input power (kW)'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        SYS1_new_equipment_rated_output = buildings('SYS1_new_equipment_rated_output', period)
        SYS1_new_efficiency = buildings('SYS1_new_efficiency', period)

        input_power = (SYS1_new_equipment_rated_output * (SYS1_new_efficiency / 100))
        return input_power


class SYS1_peak_demand_savings_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        # user input
        baseline_input_power = buildings('SYS1_baseline_input_power', period)
        baseline_peak_adjustment_factor = buildings('SYS1_baseline_peak_adjustment_factor', period)
        # temp_factor = buildings('SYS1_temperature_factor', period)
        input_power = buildings('SYS1_input_power', period)
        firmness_factor = 1

        temp1 = baseline_input_power * baseline_peak_adjustment_factor
        temp2 = input_power * baseline_peak_adjustment_factor
        
        return ((temp1 - temp2) * firmness_factor)
    
    
class SYS1_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        # user input
        peak_demand_savings_capacity = buildings('SYS1_peak_demand_savings_capacity', period)
        summer_peak_demand_reduction_duration = 6
        
        rated_output = buildings('SYS1_new_equipment_rated_output', period)        
        
        rated_output = np.select([
            (rated_output < 0.73), 
            ((rated_output >= 0.73) * (rated_output < 2.6)),    
            ((rated_output >= 2.6) * (rated_output < 9.2)),    
            ((rated_output >= 9.2) * (rated_output < 41)),    
            ((rated_output >= 41) * (rated_output < 100)),    
            ((rated_output >= 100) * (rated_output < 185)),    
            (rated_output > 185), 
        ],
        [
            'under_0.73_kW',
            '0.73_to_2.6kW',
            '2.6_to_9.2kW',
            '9.2_to_41kW',
            '41_to_100kW',
            '100_to_185kW',
            'over_185kW'
        ]
        )

        lifetime = parameters(period).ESS.HEAB.table_F7_4.asset_life[rated_output]

        return peak_demand_savings_capacity * summer_peak_demand_reduction_duration * lifetime
    
    
class SYS1_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'output'
    }
    
    def formula(buildings, period, parameters):
        peak_demand_reduction_capacity = buildings('SYS1_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('SYS1_network_loss_factor', period) 
        
        result = (peak_demand_reduction_capacity * network_loss_factor * 10)
        
        result_to_return = np.select([
                result <= 0, result > 0
            ], [
                0, result
            ])
        
        return result_to_return
