from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class BusinessClassification(Enum):
    division_A = 'Business is a Division A (Agricultural, Forestry and Fishing) business.'
    division_B = 'Business is a Division B (Mining) business.'
    division_C = 'Business is a Division C (Manufacturing) business.'
    division_D = 'Business is a Division D (Electricity, Gas, Water and Waste Services) business.'
    division_E = 'Business is a Division E (Construction) business.'
    division_F = 'Business is a Division F (Wholesale Trade) business.'
    division_G = 'Business is a Division G (Retail Trade) business.'
    division_H = 'Business is a Division H (Accommodation and Food Services) business.'
    division_I = 'Business is a Division I (Transport, Postal and Warehousing) business.'
    division_J = 'Business is a Division J (Information Media and Telecommunications) business.'
    division_K = 'Business is a Division K (Financial and Insurance Services) business.'
    division_L = 'Business is a Division L (Rental, Hiring and Real Estate Services) business.'
    division_M = 'Business is a Division M (Professional, Scientific and Technical Services) business.'
    division_N = 'Business is a Division N (Administrative and Support Services) business.'
    division_O = 'Business is a Division O (Public Administration and Safety) business.'
    division_P = 'Business is a Division P (Education and Training) business.'
    division_Q = 'Business is a Division Q (Health Care and Social Assistance) business.'
    division_R = 'Business is a Division R (Arts and Recreation Services) business.'
    division_S = 'Business is a Division S (Other Services) business.'


class ANZSIC_business_classification(Variable):
    value_type = Enum
    entity = Building
    possible_values = BusinessClassification
    default_value = BusinessClassification.division_S
    definition_period = ETERNITY
    label = 'What is the ANZSIC Classification of the business' \
            ' where the activity is taking place?'


class EndUseServices(Enum):
    air_compression = 'The End Use Service is for air compression.'
    air_handling = 'The End Use Service is for air handling, fans or ventilation.'
    air_heating_and_cooling = 'The End Use Service is for air heating and cooling.'
    cleaning_or_washing = 'The End Use Service is for cleaning or washing.'
    communications = 'The End Use Service is for communications.'
    cooking = 'The End Use Service is for cooking.'
    electricity_supply = 'The End Use Service is for electricity supply.'
    home_entertainment = 'The End Use Service is for home entertainment.'
    lighting = 'The End Use Service is for lighting.'
    liquid_pumping = 'The End Use Service is for water or liquid pumping.'
    materials_handling = 'The End Use Service is for materials handling and conveying.'
    milling_mixing_or_grinding = 'The End Use Service is for milling, mixing or grinding.'
    office_equipment = 'The End Use Service is for computers or office equipment.'
    other_end_use_services = 'The End Use Service is for other end use services, as published by the Scheme Administrator.'
    other_machines = 'The End Use Service is for other machines.'
    people_movement = 'The End Use Service is for people movement, lifts or escalators.'
    process_drives = 'The End Use Service is for process drives.'
    process_heat = 'The End Use Service is for process heat.'
    refrigeration = 'The End Use Service is for refrigeration and freezing.'
    transport = 'The End Use Service is for transport.'
    unknown = 'The End Use Service is unknown.'
    water_heating = 'The End Use Service is for water heating.'


class ESS_PDRS_End_Use_Service(Variable):
    value_type = Enum
    entity = Building
    possible_values = EndUseServices
    default_value = EndUseServices.unknown
    definition_period = ETERNITY
    label = 'What is the End Use Service for the Implementation?'
