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
    


class SYS1_new_equipment_rated_output(Variable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Rated output of new equipment (kW)'
    metadata = {
        'display_question' : 'What is the Rated Output of your new electric motor?',
        'sorting' : 3,
        'label': 'Rated output of new equipment (kW)',
        'variable-type': 'user-input'
    }


class SYS1_existing_equipment_rated_output(Variable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Rated output of existing equipment (kW)'
    metadata = {
        'display_question' : 'What is the Rated Output of your existing electric motor?',
        'sorting' : 5,
        'label': 'Rated output of existing equipment (kW)',
        'variable-type': 'user-input'
    }
    
    
class SYS1_new_efficiency(Variable):
    reference = 'percent'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Efficiency of new equipment (%)'
    metadata = {
        'display_question' : 'What is the full load efficiency of your new electric motor?',
        'sorting' : 4,
        'label': 'Efficiency of new equipment (%)'
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
        'display_question': 'Who is your Distribution Network Service Provider?',
        'sorting' : 2,
        'label': "Distribution Network Service Provider"
    }


class SYS1_baseline_efficiency(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        SYS1_new_equipment_rated_output = buildings('SYS1_existing_equipment_rated_output', period)
        # SYS1_new_efficiency = buildings('SYS1_new_efficiency', period)
        SYS1_motor_frequency = buildings('SYS1_motor_frequency', period)
        SYS1_no_of_poles = buildings('SYS1_no_of_poles', period)
        
        be = np.select( [ 
                         SYS1_motor_frequency == SYS1_motor_frequency_Options.motor_50_hz,
                         SYS1_motor_frequency == SYS1_motor_frequency_Options.motor_60_hz
                         ],
                       [
                           parameters(period).PDRS.motors.motors_baseline_efficiency_50hz[SYS1_no_of_poles]['rated_output'].calc(
            SYS1_new_equipment_rated_output, interpolate=True),
                           parameters(period).PDRS.motors.motors_baseline_efficiency_60hz[SYS1_no_of_poles]['rated_output'].calc(
            SYS1_new_equipment_rated_output, interpolate=True)
                       ])

        return be
    

class SYS1_motor_frequency_Options(Enum):
    motor_50_hz = '50 hz'
    motor_60_hz = '60 hz'


class SYS1_motor_frequency(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS1_motor_frequency_Options
    default_value = SYS1_motor_frequency_Options.motor_50_hz
    definition_period = ETERNITY
    label = "Motor Frequency (hz)"
    metadata = {
        'variable-type': 'user-input',
        'display_question': 'What is the frequency of your existing motor power supply?',
        'sorting' : 6,
        'label': "Motor Frequency (hz)"
    }


class SYS1_no_of_poles_Options(Enum):
    two_poles = '2 poles'
    four_poles = '4 poles'
    six_poles = '6 poles'
    eight_poles = '8 poles'


class SYS1_no_of_poles(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS1_no_of_poles_Options
    default_value = SYS1_no_of_poles_Options.two_poles
    definition_period = ETERNITY
    label = "Number of poles"
    metadata = {
        'variable-type': 'user-input',
        'display_question': 'How many poles is your existing motor?',
        'sorting' : 7,
        'label': "Number of poles"
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
        'display_question': 'What is the business classification?',
        'sorting' : 7,
        'label': "End User Service"
    }
    
    
class SYS1_end_user_service_Options(Enum):
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


class SYS1_end_user_service(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS1_end_user_service_Options
    default_value = SYS1_end_user_service_Options.unknown
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'user-input',
        'display_question': 'What is the End Use Service for the Implementation?',
        'sorting' : 7,
        'label': "End User Service"
    }
