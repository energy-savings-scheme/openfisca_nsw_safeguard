import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class BESS1_new_installation(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is this activity the installation of a new residential solar battery?',
        'sorting' : 1,
        'eligibility_clause' : """A replacement solar battery is not eligible under PDRS Activity BESS1. In PDRS BESS1 the activity definition states that the activity must be the installation of a new behind the meter residential battery energy storage system."""
    }
    

class BESS1_new_solar_battery(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is this the first solar battery installed at this address?',
        'sorting' : 2,
        'eligibility_clause' : """In PDRS BESS1 Eligibility Requirements Clause 1 it states that there must not be an existing battery installed at the same National Metering Identifier."""
    }


class BESS1_solar_panels(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Are there solar panels already installed at this address?',
        'sorting' : 3,
        'eligibility_clause' : """In PDRS BESS1 Eligibility Requirements Clause 2 it states that a behind the meter solar photovoltaic system must be installed at the same National Metering Identifier that the End-User Equipment is being installed."""
    }


class BESS1_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Was or will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 4,
        'eligibility_clause' : """In PDRS Clause 6 it states that an Accredited Certificate Provider may only create Peak Reduction Certificates for a Recognised Peak Activity if:<br />
                                  (a) the Accredited Certificate Provider is accredited in respect of the activity on or before the Implementation Date for the activity."""
    }


class BESS1_minimum_payment(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Are you aware that you are required to make a minimum payment towards the cost of your upgrade?',
        'sorting' : 5,
        'eligibility_clause' : """In PDRS Clause 8.3.1 it states that the Purchaser has paid a net amount of at least $200 (excluding GST) which must not be reimbursed, for the Implementation, assessment and other associated works carried out at the Site, and which payment is evidenced to the satisfaction of the Scheme Administrator, unless delivered through a Low-income Energy Program or an Exempt Energy Program."""
    }


class BESS1_battery_capacity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery capacity between 2-28kWh?',
        'sorting' : 6,
        'eligibility_clause' : """In PDRS BESS1 Eligibility Requirements Clause 2 it states that The End-User Equipment must have a usable battery capacity greater than 2 kWh and less than 28 kWh as recorded on the approved product list specified by the Scheme Administrator."""
    }
    

class BESS1_battery_warranty(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the battery have a warranty of at least 7 years?',
        'sorting' : 7,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 4 it states that the End-User Equipment must have a warranty of at least 7 years. """
    }


class BESS1_battery_internet_connectable(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery internet connectable?',
        'sorting' : 8,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 3 it states that the End-User Equipment must be internet connectable and controllable by a Demand Response Aggregator."""
    }


class BESS1_battery_controllable_third_party(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery controllable by a third party energy retailer or service provider?',
        'sorting' : 9,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 3 it states that the End-User Equipment must be internet connectable and controllable by a Demand Response Aggregator."""
    }


class BESS1_approved_list(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the installed battery a registered product on the Clean Energy Council approved battery list?',
        'sorting' :10,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 1 it states that the End-User Equipment must be listed on the approved product list specified by the Scheme Administrator"""
    }


class BESS1_equipment_installation(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the installation of the end-user equipment been performed by an installer that is on the Clean Energy Council approved installer list?',
        'sorting' : 11,
        'eligibility_clause' : """In PDRS BESS1 Implementation Requirements clause 2 it states that the End-User Equipment must be installed by an installer that is on the approved installer list specified by the Scheme Administrator.<br />
                                  In PDRS BESS1 Implementation Requirements Clause 3 its states that The activity must be performed by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class BESS1_DER_register(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the battery installation been registered on the AEMO Distributed Energy Resource (DER) Register?',
        'sorting' : 12,
        'eligibility_clause' : """In PDRS BESS1 Implementation Requirements Clause 4 it states that the installation of the End-User Equipment must be registered on the DER Register."""
    }
