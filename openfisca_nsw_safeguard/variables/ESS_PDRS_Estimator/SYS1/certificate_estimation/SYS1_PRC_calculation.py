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

        baseline_input_power = SYS1_new_equipment_rated_output / (SYS1_baseline_efficiency/100)
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

        input_power = (SYS1_new_equipment_rated_output / (SYS1_new_efficiency / 100))
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
    

class SYS1_motor_frequency_Options(Enum):
    motor_50_hz = '50 Hz'
    motor_60_hz = '60 Hz'


class SYS1_new_equipment_motor_frequency_peak_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS1_motor_frequency_Options
    default_value = SYS1_motor_frequency_Options.motor_50_hz
    definition_period = ETERNITY
    label = "Motor frequency (Hz)"
    metadata = {
        'variable-type': 'user-input',
        'label': 'Motor frequency (Hz)',
        'display_question' : 'What is the frequency of your new motor power supply?',
        'sorting' : 8
    }


class SYS1_no_of_poles_Options(Enum):
    poles_2 = '2 poles'
    poles_4 = '4 poles'
    poles_6 = '6 poles'
    poles_8 = '8 poles'


class SYS1_new_equipment_no_of_poles_peak_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS1_no_of_poles_Options
    default_value = SYS1_no_of_poles_Options.poles_2
    definition_period = ETERNITY
    label = "Number of poles"
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Number of poles',
        'display_question' : 'How many poles is your new motor?',
        'sorting' : 9
    }


class SYS1_existing_equipment_no_of_poles_peak_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS1_no_of_poles_Options
    default_value = SYS1_no_of_poles_Options.poles_2
    definition_period = ETERNITY
    label = "Number of poles"
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Number of poles',
        'display_question' : 'How many poles is your existing motor?',
        'sorting' : 12
    }

class SYS1_peak_demand_annual_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand annual savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #new equipment baseline efficiency
        new_equipment_rated_output = buildings('SYS1_new_equipment_rated_output', period)
        motor_frequency = buildings('SYS1_new_equipment_motor_frequency', period)
        no_of_poles = buildings('SYS1_new_equipment_no_of_poles', period)

        frequency = np.select(
            [ 
                motor_frequency == SYS1_motor_frequency_Options.motor_50_hz,
                motor_frequency == SYS1_motor_frequency_Options.motor_60_hz
            ],
            [ 
                '50hz',
                '60hz'
            ])

        node = parameters(period).PDRS.motors.motors_baseline_efficiency

        poles_2_value_50hz = node["poles_2"].rated_output.calc(
            new_equipment_rated_output, interpolate=True)
        poles_4_value_50hz = node["poles_4"].rated_output.calc(
            new_equipment_rated_output, interpolate=True)
        poles_6_value_50hz = node["poles_6"].rated_output.calc(
            new_equipment_rated_output, interpolate=True)
        poles_8_value_50hz = node["poles_8"].rated_output.calc(
            new_equipment_rated_output, interpolate=True)

        poles_2_value_60hz = node["poles_2_60hz"].rated_output.calc(
            new_equipment_rated_output, interpolate=True)
        poles_4_value_60hz = node["poles_4_60hz"].rated_output.calc(
            new_equipment_rated_output, interpolate=True)
        poles_6_value_60hz = node["poles_6_60hz"].rated_output.calc(
            new_equipment_rated_output, interpolate=True)
        poles_8_value_60hz = node["poles_8_60hz"].rated_output.calc(
            new_equipment_rated_output, interpolate=True)

        new_equipment_baseline_efficiency = np.select([
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_peak_savings.possible_values.poles_2, frequency == '50hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_peak_savings.possible_values.poles_4, frequency == '50hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_peak_savings.possible_values.poles_6, frequency == '50hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_peak_savings.possible_values.poles_8, frequency == '50hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_peak_savings.possible_values.poles_2, frequency == '60hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_peak_savings.possible_values.poles_4, frequency == '60hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_peak_savings.possible_values.poles_6, frequency == '60hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_peak_savings.possible_values.poles_8, frequency == '60hz')
            ],
            [
                poles_2_value_50hz, 
                poles_4_value_50hz,
                poles_6_value_50hz, 
                poles_8_value_50hz, 
                poles_2_value_60hz,
                poles_4_value_60hz,
                poles_6_value_60hz,
                poles_8_value_60hz
            ])

        #baseline input power
        baseline_input_power = new_equipment_rated_output / (new_equipment_baseline_efficiency /100)

        #BCA climate zozne  
        postcode = buildings('SYS1_PDRS__postcode', period)
        # Returns an integer
        climate_zone = parameters(period).ESS.ESS_general.table_A26_BCA_climate_zone_by_postcode       
        climate_zone_int = climate_zone.calc(postcode)
        climate_zone_savings = np.select(
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

        #baseline peak adjustment factor
        temp_factor = parameters(period).PDRS.table_A28_temperature_factor.temperature_factor[climate_zone_savings]        
        usage_factor = 0.6

        baseline_peak_adjustment_factor = temp_factor * usage_factor

        #input power
        new_efficiency = buildings('SYS1_new_efficiency', period)

        input_power = (new_equipment_rated_output / (new_efficiency / 100))
        
        firmness_factor = 1
        summer_peak_demand_reduction_duration = 6

        temp1 = baseline_input_power * baseline_peak_adjustment_factor
        temp2 = input_power * baseline_peak_adjustment_factor

        peak_demand_annual_savings = ((temp1 - temp2) * firmness_factor) * summer_peak_demand_reduction_duration
        
        peak_demand_annual_savings_return = np.select([
                peak_demand_annual_savings <= 0, peak_demand_annual_savings > 0
            ], 
            [
                0, peak_demand_annual_savings
            ])
        
        return peak_demand_annual_savings_return
        

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
            ((rated_output >= 100) * (rated_output <= 185)),    
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
        network_loss_factor = buildings('SYS1_get_network_loss_factor_by_postcode', period) 

        result = (peak_demand_reduction_capacity * network_loss_factor * 10)
        
        result_to_return = np.select([
                result <= 0, result > 0
            ], [
                0, result
            ])
        
        return result_to_return
