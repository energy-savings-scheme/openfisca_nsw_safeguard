from xml.etree import ElementInclude
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class SYS1_asset_life(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = "High Efficiency Motor Asset Life"
    metadata = {
        'variable-type': 'inter-interesting',
        'label': "High Efficiency Motor Asset Life"
    }
    
    def formula(buildings, period, parameters):
        rated_output = buildings('SYS1_new_equipment_rated_output', period)
        rated_output_band = np.select([
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
        asset_life = parameters(period).ESS.HEAB.table_F7_4['asset_life'][rated_output_band]        
        return asset_life


class SYS1_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        replacement_activity = buildings('SYS1_replacement_activity', period)
        new_equipment_rated_output = buildings('SYS1_new_equipment_rated_output', period)
        new_equipment_baseline_efficiency = buildings('SYS1_new_equipment_baseline_efficiency', period)
        existing_equipment_baseline_efficiency = buildings('SYS1_existing_equipment_baseline_efficiency', period)
        new_efficiency = buildings('SYS1_new_efficiency', period)
        load_utilisation_factor = buildings('SYS1_load_utilisation_factor', period)
        asset_life = buildings('SYS1_asset_life', period)

        new_vs_existing_equipment_baseline = np.select(
            [
                np.logical_not(replacement_activity), #new install
                replacement_activity,
            ],
            [
                new_equipment_baseline_efficiency,
                existing_equipment_baseline_efficiency
            ])
            
        temp_calc_1 = ( new_equipment_rated_output / (new_vs_existing_equipment_baseline / 100))
        temp_calc_2 = ( new_equipment_rated_output / (new_efficiency / 100))
        temp_calc_3 = (load_utilisation_factor * asset_life * ( 8760 / 1000 ))

        return ((temp_calc_1 - temp_calc_2) * temp_calc_3)


class SYS1_motor_frequency_Options(Enum):
    motor_50_hz = '50 Hz'
    motor_60_hz = '60 Hz'


class SYS1_new_equipment_motor_frequency_savings(Variable):
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


class SYS1_new_equipment_no_of_poles_savings(Variable):
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


class SYS1_existing_equipment_no_of_poles_savings(Variable):
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

class SYS1_BusinessClassification_Options(Enum):
    unknown = 'Unknown'
    division_A = 'Division A (Agricultural, Forestry and Fishing) business'
    division_B = 'Division B (Mining) business'
    division_C = 'Division C (Manufacturing) business'
    division_D = 'Division D (Electricity, Gas, Water and Waste Services) business'
    division_E = 'Division E (Construction) business'
    division_F = 'Division F (Wholesale Trade) business'
    division_G = 'Division G (Retail Trade) business'
    division_H = 'Division H (Accommodation and Food Services) business'
    division_I = 'Division I (Transport, Postal and Warehousing) business'
    division_J = 'Division J (Information Media and Telecommunications) business'
    division_K = 'Division K (Financial and Insurance Services) business'
    division_L = 'Division L (Rental, Hiring and Real Estate Services) business'
    division_M = 'Division M (Professional, Scientific and Technical Services) business'
    division_N = 'Division N (Administrative and Support Services) business'
    division_O = 'Division O (Public Administration and Safety) business'
    division_P = 'Division P (Education and Training) business'
    division_Q = 'Division Q (Health Care and Social Assistance) business'
    division_R = 'Division R (Arts and Recreation Services) business'
    division_S = 'Division S (Other Services) business'


class SYS1_business_classification_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS1_BusinessClassification_Options
    default_value = SYS1_BusinessClassification_Options.unknown
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'user-input',
        'label' : 'Business Classification',
        'display_question' : 'What is the business classification of your new electric motor?',
        'sorting' : 4
    }
    
    
class SYS1_end_use_service_Options(Enum):
    unknown = 'Unknown'
    air_compression = 'Air compression'
    air_handling = 'Air handling, fans or ventilation'
    air_heating_and_cooling = 'Air heating and cooling'
    cleaning_or_washing = 'Cleaning or washing'
    communications = 'Communications'
    cooking = 'Cooking'
    electricity_supply = 'Electricity supply'
    home_entertainment = 'Home entertainment'
    lighting = 'Lighting'
    liquid_pumping = 'Water or liquid pumping'
    materials_handling = 'Materials handling and conveying'
    milling_mixing_or_grinding = 'Milling, mixing or grinding'
    office_equipment = 'Computers or office equipment'
    people_movement = 'People movement, lifts or escalators'
    process_drives = 'Process drives'
    process_heat = 'Process heat'
    refrigeration = 'Refrigeration and freezing'
    transport = 'Transport'
    water_heating = 'Water heating'


class SYS1_end_use_service_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS1_end_use_service_Options
    default_value = SYS1_end_use_service_Options.unknown
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'End Use Service',
        'display_question' : 'What is the End Use Service for the implementation?',
        'sorting' : 5
    }


class SYS1_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #replacement activity
        replacement_activity = buildings('SYS1_replacement_activity', period)

        #new equipment rated output
        new_equipment_rated_output = buildings('SYS1_new_equipment_rated_output', period)

        #new equipment baseline efficiency
        motor_frequency = buildings('SYS1_new_equipment_motor_frequency', period)
        no_of_poles = buildings('SYS1_new_equipment_no_of_poles', period)
        
        frequency = np.select( [ 
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
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_savings.possible_values.poles_2, frequency == '50hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_savings.possible_values.poles_4, frequency == '50hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_savings.possible_values.poles_6, frequency == '50hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_savings.possible_values.poles_8, frequency == '50hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_savings.possible_values.poles_2, frequency == '60hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_savings.possible_values.poles_4, frequency == '60hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_savings.possible_values.poles_6, frequency == '60hz'),
                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles_savings.possible_values.poles_8, frequency == '60hz')
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

        #existing equipment baseline efficiency
        existing_equipment_rated_output = buildings('SYS1_existing_equipment_rated_output', period)
        no_of_poles = buildings('SYS1_existing_equipment_no_of_poles', period)
        
        frequency = np.select( [ 
                         motor_frequency == SYS1_motor_frequency_Options.motor_50_hz,
                         motor_frequency == SYS1_motor_frequency_Options.motor_60_hz
            ],
            [ 
                '50hz',
                '60hz'
            ])
        
        node = parameters(period).PDRS.motors.motors_baseline_efficiency
        
        poles_2_value_50hz = node["poles_2"].rated_output.calc(
            existing_equipment_rated_output, interpolate=True)
        poles_4_value_50hz = node["poles_4"].rated_output.calc(
            existing_equipment_rated_output, interpolate=True)
        poles_6_value_50hz = node["poles_6"].rated_output.calc(
            existing_equipment_rated_output, interpolate=True)
        poles_8_value_50hz = node["poles_8"].rated_output.calc(
            existing_equipment_rated_output, interpolate=True)

        poles_2_value_60hz = node["poles_2_60hz"].rated_output.calc(
            existing_equipment_rated_output, interpolate=True)
        poles_4_value_60hz = node["poles_4_60hz"].rated_output.calc(
            existing_equipment_rated_output, interpolate=True)
        poles_6_value_60hz = node["poles_6_60hz"].rated_output.calc(
            existing_equipment_rated_output, interpolate=True)
        poles_8_value_60hz = node["poles_8_60hz"].rated_output.calc(
            existing_equipment_rated_output, interpolate=True)
        
        existing_equipment_baseline_efficiency = np.select([
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles_savings.possible_values.poles_2, frequency == '50hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles_savings.possible_values.poles_4, frequency == '50hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles_savings.possible_values.poles_6, frequency == '50hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles_savings.possible_values.poles_8, frequency == '50hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles_savings.possible_values.poles_2, frequency == '60hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles_savings.possible_values.poles_4, frequency == '60hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles_savings.possible_values.poles_6, frequency == '60hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles_savings.possible_values.poles_8, frequency == '60hz')
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
                                                ], 0)

        #new efficiency
        new_efficiency = buildings('SYS1_new_efficiency', period)

        #luf
        business_classification = buildings('SYS1_business_classification', period)
        end_use_service = buildings('SYS1_end_use_service', period)
        
        rated_output = np.select(
            [
                (new_equipment_rated_output < 0.73), 
                ((new_equipment_rated_output >= 0.73) * (new_equipment_rated_output < 2.6)),    
                ((new_equipment_rated_output >= 2.6) * (new_equipment_rated_output < 9.2)),    
                ((new_equipment_rated_output >= 9.2) * (new_equipment_rated_output < 41)),    
                ((new_equipment_rated_output >= 41) * (new_equipment_rated_output < 100)),    
                ((new_equipment_rated_output >= 100) * (new_equipment_rated_output <= 185)),    
                (new_equipment_rated_output > 185),
            ],
            [
                'under_0.73_kW',
                '0.73_to_2.6kW',
                '2.6_to_9.2kW',
                '9.2_to_41kW',
                '41_to_100kW',
                '100_to_185kW',
                'over_185kW'
            ])

        load_utilisation_factor = np.select(
            [
                (business_classification != SYS1_BusinessClassification_Options.unknown) * (end_use_service != SYS1_end_use_service_Options.unknown),
                (business_classification != SYS1_BusinessClassification_Options.unknown) * (end_use_service == SYS1_end_use_service_Options.unknown),
                (business_classification == SYS1_BusinessClassification_Options.unknown) * (end_use_service != SYS1_end_use_service_Options.unknown),
                (business_classification == SYS1_BusinessClassification_Options.unknown) * (end_use_service == SYS1_end_use_service_Options.unknown)
            ],
            [
                parameters(period).ESS.HEAB.table_F7_1['load_utilisation_factor'][business_classification][end_use_service],
                parameters(period).ESS.HEAB.table_F7_2['load_utilisation_factor'][rated_output],
                parameters(period).ESS.HEAB.table_F7_2['load_utilisation_factor'][rated_output],
                parameters(period).ESS.HEAB.table_F7_2['load_utilisation_factor'][rated_output]
            ])

        #asset life
        rated_output_band = np.select([
                (new_equipment_rated_output < 0.73), 
                ((new_equipment_rated_output >= 0.73) * (new_equipment_rated_output < 2.6)),    
                ((new_equipment_rated_output >= 2.6) * (new_equipment_rated_output < 9.2)),    
                ((new_equipment_rated_output >= 9.2) * (new_equipment_rated_output < 41)),    
                ((new_equipment_rated_output >= 41) * (new_equipment_rated_output < 100)),    
                ((new_equipment_rated_output >= 100) * (new_equipment_rated_output <= 185)),    
                (new_equipment_rated_output > 185)
            ],
            [
                'under_0.73_kW',
                '0.73_to_2.6kW',
                '2.6_to_9.2kW',
                '9.2_to_41kW',
                '41_to_100kW',
                '100_to_185kW',
                'over_185kW'
            ])
        asset_life = parameters(period).ESS.HEAB.table_F7_4['asset_life'][rated_output_band]      

        new_vs_existing_equipment_baseline = np.select(
            [
                np.logical_not(replacement_activity), #new install
                replacement_activity,
            ],
            [
                new_equipment_baseline_efficiency,
                existing_equipment_baseline_efficiency
            ])
            
        #deemed electricity savings
        temp_calc_1 = ( new_equipment_rated_output / (new_vs_existing_equipment_baseline / 100))
        temp_calc_2 = ( new_equipment_rated_output / (new_efficiency / 100))
        temp_calc_3 = (load_utilisation_factor * asset_life * ( 8760 / 1000 ))

        #deemed electricity savings
        deemed_electricity_savings = ((temp_calc_1 - temp_calc_2) * temp_calc_3)
        
        #regional network factor
        postcode = buildings('SYS1_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        regional_network_factor = rnf.calc(postcode)

        #electricity savings
        annual_savings = (deemed_electricity_savings * regional_network_factor)
        
        annual_savings_return = np.select([
            annual_energy_savings <= 0, annual_energy_savings > 0
        ], [
            0, annual_energy_savings
        ])
        
        return annual_savings_return
      

class SYS1_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('SYS1_deemed_activity_electricity_savings', period)
        regional_network_factor = buildings('SYS1_regional_network_factor', period)
        return deemed_electricity_savings * regional_network_factor


class SYS1_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for SYS1'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('SYS1_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06

        result = (electricity_savings * electricity_certificate_conversion_factor)
        result_to_return = np.select([
                result < 0, result > 0
            ], [
                0, result
            ])
        return result_to_return