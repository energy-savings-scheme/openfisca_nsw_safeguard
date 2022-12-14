import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class SYS1_regional_network_factor(Variable):
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
        postcode = buildings('SYS1_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided
    

class SYS1_replacement_activity(Variable):
    value_type = bool
    default_value = False
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Replacement or new installation activity',
        'display_question' : 'Is the activity a replacement of existing equipment?',
        'sorting' : 3
        }


class SYS1_new_equipment_rated_output(Variable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Rated output of new equipment (kW)'
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Rated output of new equipment (kW). The electric motor must have a rated output rated output from 0.73kW to <185kW.',
        'display_question' : 'What is the Rated Output of your new electric motor?',
        'sorting' : 7
    }


class SYS1_existing_equipment_rated_output(Variable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Rated output of existing equipment (kW)'
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Rated output of existing equipment (kW)',
        'display_question' : 'What is the Rated Output of your existing electric motor?',
        'sorting' : 10
    }

    
class SYS1_new_efficiency(Variable):
    reference = 'percent'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Efficiency of new equipment (%)'
    metadata = {
        'label': 'Efficiency of new equipment (%)',
        'display_question' : 'What is the full load efficiency of your new electric motor?',
        'sorting' : 6 
    }


class SYS1_DNSP_Options(Enum):
    Ausgrid = 'Ausgrid'
    Endeavour = 'Endeavour'
    Essential = 'Essential'


class SYS1_DNSP(Variable):
     # this variable is used as the second input on all estimator certificate calculation pages
    value_type = Enum
    entity = Building
    possible_values = SYS1_DNSP_Options
    default_value = SYS1_DNSP_Options.Ausgrid
    definition_period = ETERNITY
    label = "Distribution Network Service Provider"
    metadata = {
        'variable-type': 'user-input',
        'label': "Distribution Network Service Provider",
        'display_question' : 'Who is your Distribution Network Service Provider?',
        'sorting' : 2
    }


class SYS1_new_equipment_baseline_efficiency(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        new_equipment_rated_output = buildings('SYS1_new_equipment_rated_output', period)
        motor_frequency = buildings('SYS1_new_equipment_motor_frequency', period)
        no_of_poles = buildings('SYS1_new_equipment_no_of_poles', period)
        
        frequency = np.select( [ 
                         motor_frequency == SYS1_motor_frequency_Options.motor_50_hz,
                         motor_frequency == SYS1_motor_frequency_Options.motor_60_hz
                        ],
            [ 
                '50hz',
                '60hz'
            ]
        )
        
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
                                                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles.possible_values.poles_2, frequency == '50hz'),
                                                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles.possible_values.poles_4, frequency == '50hz'),
                                                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles.possible_values.poles_6, frequency == '50hz'),
                                                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles.possible_values.poles_8, frequency == '50hz'),
                                                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles.possible_values.poles_2, frequency == '60hz'),
                                                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles.possible_values.poles_4, frequency == '60hz'),
                                                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles.possible_values.poles_6, frequency == '60hz'),
                                                np.logical_and(no_of_poles == SYS1_new_equipment_no_of_poles.possible_values.poles_8, frequency == '60hz')
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

        return new_equipment_baseline_efficiency


class SYS1_existing_equipment_baseline_efficiency(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        existing_equipment_rated_output = buildings('SYS1_existing_equipment_rated_output', period)
        motor_frequency = buildings('SYS1_existing_equipment_motor_frequency', period)
        no_of_poles = buildings('SYS1_existing_equipment_no_of_poles', period)
        
        frequency = np.select( [ 
                         motor_frequency == SYS1_motor_frequency_Options.motor_50_hz,
                         motor_frequency == SYS1_motor_frequency_Options.motor_60_hz
                        ],
            [ 
                '50hz',
                '60hz'
            ]
        )
        
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
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles.possible_values.poles_2, frequency == '50hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles.possible_values.poles_4, frequency == '50hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles.possible_values.poles_6, frequency == '50hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles.possible_values.poles_8, frequency == '50hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles.possible_values.poles_2, frequency == '60hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles.possible_values.poles_4, frequency == '60hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles.possible_values.poles_6, frequency == '60hz'),
                                                    np.logical_and(no_of_poles == SYS1_existing_equipment_no_of_poles.possible_values.poles_8, frequency == '60hz')
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

        return existing_equipment_baseline_efficiency


class SYS1_motor_frequency_Options(Enum):
    motor_50_hz = '50 hz'
    motor_60_hz = '60 hz'


class SYS1_new_equipment_motor_frequency(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS1_motor_frequency_Options
    default_value = SYS1_motor_frequency_Options.motor_50_hz
    definition_period = ETERNITY
    label = "Motor Frequency (hz)"
    metadata = {
        'variable-type': 'user-input',
        'label': 'Motor Frequency (hz)',
        'display_question' : 'What is the frequency of your new motor power supply?',
        'sorting' : 8
    }


class SYS1_existing_equipment_motor_frequency(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS1_motor_frequency_Options
    default_value = SYS1_motor_frequency_Options.motor_50_hz
    definition_period = ETERNITY
    label = "Motor Frequency (hz)"
    metadata = {
        'variable-type': 'user-input',
        'label': 'Motor Frequency (hz)',
        'display_question' : 'What is the frequency of your existing motor power supply?',
        'sorting' : 11
    }


class SYS1_no_of_poles_Options(Enum):
    poles_2 = '2 poles'
    poles_4 = '4 poles'
    poles_6 = '6 poles'
    poles_8 = '8 poles'


class SYS1_new_equipment_no_of_poles(Variable):
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


class SYS1_existing_equipment_no_of_poles(Variable):
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


class SYS1_business_classification(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS1_BusinessClassification_Options
    default_value = SYS1_BusinessClassification_Options.unknown
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'user-input',
        'label' : 'Business Classification',
        'display_question' : 'What is the business classification of your new clectric motor?',
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


class SYS1_end_use_service(Variable):
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


class SYS1_load_utilisation_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input power (kW)'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        rated_output = buildings('SYS1_new_equipment_rated_output', period)
        business_classification = buildings('SYS1_business_classification', period)
        end_use_service = buildings('SYS1_end_use_service', period)
        
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

        return load_utilisation_factor