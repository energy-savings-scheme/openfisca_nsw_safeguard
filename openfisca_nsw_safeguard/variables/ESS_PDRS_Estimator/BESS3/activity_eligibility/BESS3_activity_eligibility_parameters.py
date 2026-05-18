import numpy as np
from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building



class BESS3_new_installation(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is this activity the installation of a new behind the meter battery for apartments?',
        'sorting' : 1,
        'eligibility_clause' : """A replacement solar battery is not eligible under PDRS Activity BESS3. In PDRS BESS3 the activity definition states that the activity must be the installation of a new behind the meter battery energy storage system for apartments."""
    }
    

class BESS3_apartment_dwellings(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the site a Class 2 apartment building with at least four individual dwellings at this address?',
        'sorting' : 2,
        'eligibility_clause' : """In PDRS BESS3 Eligibility Requirements Clause 1 it states that the site must be an apartment building comprising not less than four individual dwellings."""
    }


class BESS3_nmi(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is there a battery already installed at this address?',
        'sorting' : 3,
        'eligibility_clause' : """In PDRS BESS3 Eligibility Requirements Clause 2 it states that there must not be an existing Battery Energy Storage System installed at the same National Metering Identifier(s)."""
    }


class BESS3_engaged_ACP(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 4,
        'eligibility_clause' : """In PDRS Clause 6 it states that an Accredited Certificate Provider may only create Peak Reduction Certificates for a Recognised Peak Activity if:<br />
                                  (a) the Accredited Certificate Provider is accredited in respect of the activity on or before the Implementation Date for the activity on or after 1 June 2026."""
    }


class BESS3_minimum_payment(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the purchaser aware that they are required to make a minimum payment towards the cost of the upgrade?',
        'sorting' : 5,
        'eligibility_clause' : """In PDRS Clause 8.1.1 it states that the Accredited Certificate Provider has evidence satisfactory to the Scheme Administrator that the Purchaser has paid for the Implementation, assessment and other associated works carried out at the Site a Net Amount of at least $1,000 (excluding GST) for each item of End-User Equipment installed as part of an Implementation using Activity Definition BESS3;"""
    }


class BESS3_battery_capacity(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the usable battery capacity between 20 - 200kWh?',
        'sorting' : 6,
        'eligibility_clause' : """In PDRS BESS3 Eligibility Requirements Clause 2 it states that the End-User Equipment must have a Usable Battery Capacity greater than 20 kWh and less than or equal to 200 kWh as recorded on the approved product list specified by the Scheme Administrator."""
    }


class BESS3_length_battery_warranty(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the battery have a warranty of at least 10 years?',
        'sorting' : 7,
        'eligibility_clause' : """In PDRS BESS3 Equipment Requirements Clause 5 it states that each item of End-User Equipment, excluding inverters installed prior to the Implementation Date, must have a warranty of at least 10 years and guarantee that at least seventy percent (70%) of Usable Battery Capacity is retained 10 years from the date the End-User Equipment is installed at the site."""
    }


class BESS3_retainable_battery_capacity_warranty(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : "Does the warranty guarantee that at least seventy percent (70%) of the battery's usable capacity is retained 10 years from the installation date?",
        'sorting' : 8,
        'eligibility_clause' : """In PDRS BESS3 Equipment Requirements Clause 5 it states that each item of End-User Equipment, excluding inverters installed prior to the Implementation Date, must have a warranty of at least 10 years and guarantee that at least seventy percent (70%) of Usable Battery Capacity is retained 10 years from the date the End-User Equipment is installed at the site."""
    }
    

class BESS3_approved_batteries_list(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery listed on an approved product list specified by the Scheme Administrator?',
        'sorting' : 9,
        'eligibility_clause' : """In PDRS BESS3 Equipment Requirements Clause 1 it states that the End-User Equipment must be listed on an approved product list specified by the Scheme Administrator."""
    }


class BESS3_battery_inverter_output(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the battery capacity not exceed six times the battery inverter output?',
        'sorting' : 10,
        'eligibility_clause' : """In PDRS BESS3 Equipment Requirements Clause 3 it states that the Usable Battery Capacity of the End-User Equipment must not exceed six times the Battery Inverter Output of the End-User Equipment as recorded on the approved product list specified by the Scheme Administrator."""
    }


class BESS3_installation_location(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the battery be installed outdoors?',
        'sorting' : 11,
        'eligibility_clause' : """In PDRS BESS3 Implementation Requirements Clause 1 it states that the End-User Equipment must be installed outdoors."""
    }


class BESS3_behind_meter(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery installed behind the meter in accordance with AS/NZS 5139?',
        'sorting' : 12,
        'eligibility_clause' : """In PDRS BESS3 Implmentation Requirements Clause 2 it states that the End-User Equipment must be installed behind the meter and in accordance with AS/NZS 5139."""
    }


class BESS3_approved_installer_list(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the installer on the approved installer list?',
        'sorting' : 13,
        'eligibility_clause' : """In PDRS BESS3 Implementation Requirements Clause 3 it states that the End-User Equipment must be installed by an installer on an approved installer list specified by the Scheme Administrator."""
    }


class BESS3_licensed_person(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the battery be installed by a suitably licensed installer in compliance with the relevant standards and legislation?',
        'sorting' : 14,
        'eligibility_clause' : """In PDRS BESS3 Implementation Requirements Clause 4 it states that the activity must be performed by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class BESS3_internet_connectable(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery internet connectable?',
        'sorting' : 15,
        'eligibility_clause' : """In PDRS BESS3 Equipment Requirements Clause 4 it states that the End-User Equipment must be internet connectable and controllable by a Demand Response Aggregator."""
    }


class BESS3_controlled_aggregator(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery controllable by a third party energy retailer or service provider?',
        'sorting' : 16,
        'eligibility_clause' : """In PDRS BESS3 Equipment Requirements Clause 4 it states that the End-User Equipment must be internet connectable and controllable by a Demand Response Aggregator."""
    }