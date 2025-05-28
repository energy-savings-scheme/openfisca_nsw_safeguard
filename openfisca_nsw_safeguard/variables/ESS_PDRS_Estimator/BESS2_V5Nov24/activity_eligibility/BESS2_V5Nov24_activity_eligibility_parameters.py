import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class BESS2_V5Nov24_demand_response_contract(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Are you aware that you need to sign a demand response contract for your solar battery?',
        'sorting' : 1,
        'eligibility_clause' : """The PDRS BESS2 activity is to sign a behind the meter Battery Energy Storage System up to a demand response contract."""
    }


class BESS2_V5Nov24_existing_solar_battery(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is there a solar battery already installed at this address?',
        'sorting' : 2,
        'eligibility_clause' : """In PDRS BESS2 Eligibility Requirements Clause 1 it states that there must be an existing Battery Energy Storage System installed at the National Metering Identifier(s)."""
    }


class BESS2_V5Nov24_solar_panels_existing_address(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Are there solar panels already installed at this address?',
        'sorting' : 3,
        'eligibility_clause' : """In PDRS BESS2 Eligibility Requirements Clause 2 it states that a behind the meter solar photovoltaic system must be installed at the same National Metering Identifier(s) as the existing Battery Energy Storage System."""
    }
    

class BESS2_V5Nov24_life_support_equipment(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Are you aware that demand response is not allowed where there is life support equipment?',
        'sorting' : 4,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 3 it states that there must not be any Life Support Equipment used at the Site."""
    }


class BESS2_V5Nov24_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 5,
        'eligibility_clause' : """In PDRS Clause 6 it states that an Accredited Certificate Provider may only create Peak Reduction Certificates for a Recognised Peak Activity if:<br />
                                  (a) the Accredited Certificate Provider is accredited in respect of the activity on or before the Implementation Date for the activity."""
    }


class BESS2_V5Nov24_battery_capacity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery capacity between 2- 28kWh?',
        'sorting' : 6,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 2 it states that the End-User Equipment must have a Usable Battery Capacity greater than 2 kWh and less than 28 kWh as recorded on the approved product list specified by the Scheme Administrator."""
    }


class BESS2_V5Nov24_length_battery_warranty(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the battery have a remaining warranty of at least 6 years?',
        'sorting' : 7,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 3 it states that each item of End-User Equipment must have a minimum 6 years remaining on the warranty."""
    }


class BESS2_V5Nov24_temperature_range_warranty(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the warranty define the normal use conditions of the battery as a minimum ambient temperature range of -10°C to 50°C?',
        'sorting' : 8,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 4 it states that each End-User Equipment warranty must define the normal use conditions during the operation of the End-User Equipment as not being less than a minimum ambient temperature range of -10°C to 50°C."""
    }


class BESS2_V5Nov24_minimum_throughput_warranty_before_April_2026(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the warranty include a minimum throughput of 2.8MWh per kWh of usable capacity?',
        'sorting' : 9,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 4 it states that each End-User Equipment warranty must define the normal use conditions during the operation of the End-User Equipment as not being less than a minimum warranted cumulative energy throughput equivalent to 2.8 MWh per kWh of Usable Battery Capacity where the Implementation Date is before 1 April 2026."""
    }


class BESS2_V5Nov24_internet_connectable(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery internet connectable?',
        'sorting' : 10,
        'eligibility_clause' : """In PDRS BESS2 Implementation Requirements Clause 1 it states that the internet connection and Demand Response Aggregator control of the End-User Equipment must be demonstrated to be operational to the satisfaction of the Scheme Administrator."""
    }


class BESS2_V5Nov24_battery_controllable_third_party(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery controllable by a third party energy retailer or service provider?',
        'sorting' : 11,
        'eligibility_clause' : """In PDRS BESS2 Implementation Requirements Clause 1 it states that the internet connection and Demand Response Aggregator control of the End-User Equipment must be demonstrated to be operational to the satisfaction of the Scheme Administrator."""
    }


class BESS2_V5Nov24_approved_battery_list(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery a registered product on the Clean Energy Council approved battery list?',
        'sorting' : 12,
        'eligibility_clause' : """In PDRS BESS2 Equipment Requirements Clause 1 it states that the End-User Equipment must be listed on the approved product list specified by the Scheme Administrator."""
    }