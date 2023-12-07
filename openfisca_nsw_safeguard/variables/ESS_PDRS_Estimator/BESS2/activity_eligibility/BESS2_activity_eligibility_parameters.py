import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class BESS2_demand_response_contract(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Have you signed a demand response contract for your residential solar battery?',
        'sorting' : 1,
        'eligibility_clause' : """A replacement solar battery is not eligible under PDRS Activity BESS2. In PDRS BESS2 the activity definition states that the activity must be sign a behind the meter residential battery energy storage system up to a demand response contract."""
    }


class BESS2_existing_solar_battery(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is there an existing solar battery already installed at this address?',
        'sorting' : 2,
        'eligibility_clause' : """In PDRS BESS2 Eligibility Requirements Clause 1 it states that there must be an existing battery energy storage system installed at the National Metering Identifier."""
    }


class BESS2_solar_panels_existing_address(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Are there solar panels already installed at the existing address?',
        'sorting' : 3,
        'eligibility_clause' : """In PDRS BESS2 Eligibility Requirements Clause 2 it states that a behind the meter solar photovoltaic system must be installed at the same National Metering Identifier as the existing battery energy storage system."""
    }
    

class BESS2_life_support_equipment(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Are you aware that demand response is not allowed where there is life support equipment?',
        'sorting' : 4,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 3 it states that there must not be any Life Support Equipment used at the Site."""
    }


class BESS2_battery_capacity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery capacity between 2- 28kWh?',
        'sorting' : 5,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 2 it states that the End-User Equipment must have a usable battery capacity greater than 2 kWh and less than 28 kWh as recorded on the approved product list specified by the Scheme Administrator."""
    }


class BESS2_implementation_date(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Was the battery installed within the last seven years?',
        'sorting' : 6,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements clause 3 it states that the End-User Equipment must have an installation date within 7 years of the Implementation Date as listed on the DER Register."""        
    }


class BESS2_internet_connectable(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery internet connectable?',
        'sorting' : 7,
        'eligibility_clause' : """In PDRS BESS2 Implementation Requirements clause 1 it states that the internet connection and Demand Response Aggregator control of the End-User Equipment must be demonstrated to be operational to the satisfaction of the Scheme Administrator."""
    }


class BESS2_battery_controllable_third_party(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery controllable by a third party energy retailer or service provider?',
        'sorting' : 8,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 3 it states that the End-User Equipment must be internet connectable and controllable by a Demand Response Aggregator."""
    }


class BESS2_approved_battery_list(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery a registered product on the Clean Energy Council approved battery list?',
        'sorting' : 9,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements clause 1 it states that the End-User Equipment must be listed on the approved product list specified by the Scheme Administrator."""
    }