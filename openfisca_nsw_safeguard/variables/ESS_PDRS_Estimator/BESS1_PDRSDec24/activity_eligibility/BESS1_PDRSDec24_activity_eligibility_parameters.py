import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class BESS1_PDRSDec24_new_installation(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is this activity the installation of a new solar battery?',
        'sorting' : 1,
        'eligibility_clause' : """A replacement solar battery is not eligible under PDRS Activity BESS1. In PDRS BESS1 the activity definition states that the activity must be the installation of a new behind the meter battery energy storage system."""
    }
    

class BESS1_PDRSDec24_new_solar_battery(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is this the first solar battery installed at this address?',
        'sorting' : 2,
        'eligibility_clause' : """In PDRS BESS1 Eligibility Requirements Clause 1 it states that there must not be an existing Battery Energy Storage System installed at the same National Metering Identifier(s)."""
    }


class BESS1_PDRSDec24_solar_panels(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Are there solar panels already installed at this address?',
        'sorting' : 3,
        'eligibility_clause' : """In PDRS BESS1 Eligibility Requirements Clause 2 it states that a behind the meter solar photovoltaic system must be installed at the same National Metering Identifier(s) that the End-User Equipment is being installed."""
    }


class BESS1_PDRSDec24_engaged_ACP(Variable):
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


class BESS1_PDRSDec24_minimum_payment(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Are you aware that you are required to make a minimum payment towards the cost of your upgrade?',
        'sorting' : 5,
        'eligibility_clause' : """In PDRS Clause 8.3.1 it states that the Accredited Certificate Provider has evidence satisfactory to the Scheme Administrator that the Purchaser has paid for the Implementation, assessment and other associated works carried out at the Site a Net Amount of at least $200 (excluding GST) for each item of End-User Equipment installed as part of an Implementation using Activity Definition BESS1."""
    }


class BESS1_PDRSDec24_battery_capacity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery capacity between 2 - 28kWh?',
        'sorting' : 6,
        'eligibility_clause' : """In PDRS BESS1 Eligibility Requirements Clause 2 it states that the End-User Equipment must have a Usable Battery Capacity greater than 2 kWh and less than 28 kWh as recorded on the approved product list specified by the Scheme Administrator."""
    }


class BESS1_PDRSDec24_length_battery_warranty(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the battery have a warranty of at least 10 years?',
        'sorting' : 7,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 4 it states that each item of End-User Equipment, excluding inverters installed prior to the Implementation Date, must have a warranty of at least 10 years and guarantee that at least seventy percent (70%) of Usable Battery Capacity is retained 10 years from the date the End-User Equipment is installed at the site."""
    }


class BESS1_PDRSDec24_retainable_battery_capacity_warranty(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : "Does the warranty guarantee that at least seventy percent (70%) of the battery's usable capacity is retained 10 years from the installation date?",
        'sorting' : 8,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 4 it states that each item of End-User Equipment, excluding inverters installed prior to the Implementation Date, must have a warranty of at least 10 years and guarantee that at least seventy percent (70%) of Usable Battery Capacity is retained 10 years from the date the End-User Equipment is installed at the site."""
    }
    

class BESS1_PDRSDec24_inverter_installed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Do you already have an inverter installed?',
        'sorting' : 9,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 5 it states that each item of End-Equipment that is a inverter installed prior to the Implementation Date must have a warranty of at least 10 years from the date that it was installed."""
    }


class BESS1_PDRSDec24_inverter_warranty(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does your inverter have a warranty of at least 10 years?',
        'sorting' : 10,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 5 it states that each item of End-Equipment that is a inverter installed prior to the Implementation Date must have a warranty of at least 10 years from the date that it was installed."""
    }

    
class BESS1_PDRSDec24_temperature_range_warranty(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the warranty define the normal use conditions of the battery as a minimum ambient temperature range of -10°C to 50°C?',
        'sorting' : 11,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 6 it states that each End-User Equipment warranty must define the normal use conditions during the operation of the End-User Equipment as not being less than:<br />
                                    (a) A minimum ambient temperature range of -10 °C to 50 °C"""
    }


class BESS1_PDRSDec24_minimum_throughput_warranty_before_April_2026(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the warranty include a minimum throughput of 2.8MWh per kWh of usable capacity?',
        'sorting' : 12,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 6 it states that each End-User Equipment warranty must define the normal use conditions during the operation of the End-User Equipment as not being less than:<br />
                                    (b) A minimum warranted cumulative energy throughput equivalent to 2.8 MWh per kWh of Usable Battery Capacity where the Implementation Date is before 1 April 2026"""
    }


class BESS1_PDRSDec24_InstallationLocation(Enum):
    installed_outdoors = 'Installed outdoors'
    installed_indoors = 'Installed indoors'


class BESS1_PDRSDec24_installation_location(Variable):
    value_type = Enum
    entity = Building
    possible_values = BESS1_PDRSDec24_InstallationLocation
    default_value = BESS1_PDRSDec24_InstallationLocation.installed_outdoors
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Where is your Battery Energy Storage System installed?',
        'sorting' : 13
    }


class BESS1_PDRSDec24_installation_location_eligible(Variable):
    """Checks if the location type is eligible
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      location_type = buildings('BESS1_PDRSDec24_installation_location', period)

      location_type_eligible = np.select(
        [
          (location_type == BESS1_PDRSDec24_InstallationLocation.installed_outdoors),
          (location_type == BESS1_PDRSDec24_InstallationLocation.installed_indoors)
        ],
        [
          True,
          True
        ])

      return location_type_eligible
    

class BESS1_PDRSDec24_smoke_alarm(Variable):
    #only show this question if the battery is installed indoors
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is a working smoke alarm installed in the immediate vicinity of the battery?',
        'sorting' : 14,
        'conditional' : 'True',
        'eligibility_clause' : """In PDRS BESS1 Implementation Requirements Clause 5 it states that where the Battery Energy Storage system is installed indoors, a working smoke alarm that meets AS 3786 must be installed in the immediate vicinity."""
    }


class BESS1_PDRSDec24_installed_indoors_has_smoke_alarm(Variable):
    """Checks if it's installed outdoors, and if it is, that a smoke alarm has been installed 
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    
    def formula(buildings, period, parameters):
      location_type = buildings('BESS1_PDRSDec24_installation_location', period)
      smoke_alarm_installed = buildings('BESS1_PDRSDec24_smoke_alarm', period)

      installed_indoors_has_smoke_alarm = np.select(
        [
          (location_type == BESS1_PDRSDec24_InstallationLocation.installed_outdoors) * smoke_alarm_installed,
          (location_type == BESS1_PDRSDec24_InstallationLocation.installed_outdoors) * np.logical_not(smoke_alarm_installed),
          (location_type == BESS1_PDRSDec24_InstallationLocation.installed_indoors) * smoke_alarm_installed,
          (location_type == BESS1_PDRSDec24_InstallationLocation.installed_indoors) * np.logical_not(smoke_alarm_installed)
        ],
        [
          True,
          True,
          True,
          False
        ])

      return installed_indoors_has_smoke_alarm


class BESS1_PDRSDec24_battery_internet_connectable(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery internet connectable?',
        'sorting' : 15,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 3 it states that the End-User Equipment must be internet connectable and controllable by a Demand Response Aggregator."""
    }


class BESS1_PDRSDec24_battery_controllable_third_party(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the battery controllable by a third party energy retailer or service provider?',
        'sorting' : 16,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 3 it states that the End-User Equipment must be internet connectable and controllable by a Demand Response Aggregator."""
    }


class BESS1_PDRSDec24_approved_product_list(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the installed battery a registered product on the Clean Energy Council approved battery list?',
        'sorting' : 17,
        'eligibility_clause' : """In PDRS BESS1 Equipment Requirements Clause 1 it states that the End-User Equipment must be listed on the approved product list specified by the Scheme Administrator."""
    }


class BESS1_PDRSDec24_approved_installer(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the installation of the End-User equipment been performed by an approved installer that is on the Solar Accreditation Australia installer list?',
        'sorting' : 18,
        'eligibility_clause' : """In PDRS BESS1 Implementation Requirements Clause 1 it states that the End-User Equipment must be installed in accordance with AS/NZS 5139.<br />
                                  In PDRS BESS1 Implementation Requirements Clause 2 it states that the End-User Equipment must be installed by an installer on an approved installer list specified by the Scheme Administrator.<br />
                                  In PDRS BESS1 Implementation Requirements Clause 3 it states that the activity must be performed by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class BESS1_PDRSDec24_DER_register(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has an application been made to register the installation on the AEMO Distributed Energy Resource (DER) Register?',
        'sorting' : 19,
        'eligibility_clause' : """The transitional arrangement in BESS1 Clause 11.6 states that BESS1 Implementation Requirement 4 does not apply to any Implementation for which an Accredited Certificate Provider applies to register the creation of certificates on or before:<br />
                                    (a) 19 June 2025 <br />
                                    (b) or where the Scheme Administrator has specified another date by notice Published under this clause - that other date.<br />
                                  <br /> 
                                  11.7 Where Implementation Requirement 4 of Activity Definition BESS1 does not apply to an Implementation due to clause 11.6:<br />
                                    (a) the following Implementation Requirement applies instead: “The ACP must have made a proper application to register the installation of the End-User Equipment on the DER Register”; and<br />
                                    (b) within 60 days of the Implementation Date, the ACP must ensure that the installation of the End-User Equipment is registered on the DER Register."""
    }