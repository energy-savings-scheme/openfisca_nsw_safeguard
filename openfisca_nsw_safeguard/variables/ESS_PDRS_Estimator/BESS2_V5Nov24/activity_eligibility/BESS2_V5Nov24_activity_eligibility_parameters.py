import numpy as np
from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building



class BESS2_V5Nov24_demand_response_contract(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Have you connected a solar battery to a virtual power plant?',
        'sorting' : 1,
        'eligibility_clause' : """The PDRS BESS2 activity is onboard a behind the meter residential battery energy storage system with a demand response aggregator."""
    }


class BESS2_V5Nov24_existing_solar_battery(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is there a solar battery already installed at this address?',
        'sorting' : 2,
        'eligibility_clause' : """In PDRS BESS2 Eligibility Requirements Clause 1 it states that there must be an existing Battery Energy Storage System installed at the National Metering Identifier(s)."""
    }
    

class BESS2_V5Nov24_life_support_equipment(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Are you aware that demand response is not allowed where there is life support equipment?',
        'sorting' : 3,
        'eligibility_clause' : """In PDRS BESS2 Eligibility Requirements Clause 3 it states that there must not be any Life Support Equipment used at the Site."""
    }


class BESS2_V5Nov24_engaged_ACP(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 4,
        'eligibility_clause' : """In PDRS Clause 6 it states that an Accredited Certificate Provider may only create Peak Reduction Certificates for a Recognised Peak Activity if:<br />
                                  (a) the Accredited Certificate Provider is accredited in respect of the activity on or before the Implementation Date for the activity."""
    }


class BESS2_V5Nov24_battery_capacity(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery capacity between 2- 50kWh?',
        'sorting' : 5,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 2 it states that the End-User Equipment must have a Usable Battery Capacity greater than 2 kWh and less than or equal to 50 kWh as recorded on the approved product list specified by the Scheme Administrator."""
    }


class BESS2_V5Nov24_length_battery_warranty(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the battery have a remaining warranty of at least 6 years?',
        'sorting' : 6,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 3 it states that each item of End-User Equipment must have a minimum 6 years remaining on the warranty."""
    }


class BESS2_V5Nov24_equipment_warranty(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does participation in the activity affect the validity of the End-User Equipment warranty?',
        'sorting' : 7,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 4 it states that participation in the activity must not void or diminish the End-User Equipment warranty."""
    }


class BESS2_V5Nov24_internet_connectable(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery internet connectable?',
        'sorting' : 8,
        'eligibility_clause' : """In PDRS BESS2 Implementation Requirements Clause 1 it states that the internet connection and Demand Response Aggregator control of the End-User Equipment must be demonstrated to be operational to the satisfaction of the Scheme Administrator."""
    }


class BESS2_V5Nov24_approved_battery_list(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery a registered product on the Clean Energy Council approved battery list?',
        'sorting' : 9,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 1 it states that the End-User Equipment must be listed on the approved product list specified by the Scheme Administrator."""
    }