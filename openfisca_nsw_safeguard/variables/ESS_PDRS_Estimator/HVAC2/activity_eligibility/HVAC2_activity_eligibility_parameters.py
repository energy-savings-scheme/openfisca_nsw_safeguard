import numpy as np
from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building


class HVAC2NewInstallationReplacement(Enum):
    new_installation_activity = 'Installation of a new air conditioner'
    replacement_activity = 'Replacement of an existing air conditioner'


class HVAC2_new_installation_or_replacement(BaseVariable):
    value_type = Enum
    entity = Building
    possible_values = HVAC2NewInstallationReplacement
    default_value = HVAC2NewInstallationReplacement.replacement_activity
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'display_question' : 'Which one of the following activities are you implementing?',
        'sorting' : 1
    }


class HVAC2_new_installation_or_replacement_eligible(BaseVariable):
    """Checks if the type of activity is eligible
    """
    value_type = bool
    entity = Building 
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      activity_type = buildings('HVAC2_new_installation_or_replacement', period)

      activity_type_eligible = np.select(
        [
          (activity_type == HVAC2NewInstallationReplacement.new_installation_activity),
          (activity_type == HVAC2NewInstallationReplacement.replacement_activity)
        ],
        [
          True,
          True
        ])

      return activity_type_eligible


class HVAC2_installed_by_qualified_person(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Will the activity be performed or supervised by a suitably licensed person in accordance with relevant standards?',
        'sorting' : 4,
        'conditional': 'True',
        'eligibility_clause' : """In PDRS HVAC2 Implementation Requirements Clause 3 it states that the activity, including the removal of any existing End-User Equipment, must be performed or supervised by a suitably qualified license holder in compliance with the relevant standards and legislation."""
    }


class HVAC2_new_ac_installed_and_operational(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Will the new End-User Equipment be installed and operational?',
        'sorting' : 5,
        'conditional': 'True',
        'eligibility_clause' : """In PDRS HVAC2 Implementation Requirements Clause 2 it states that the new End-User Equipment or replacement End-User Equipment must be installed"""
    }


class HVAC2_minimum_payment(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Are you aware that you are required to make a minimum payment towards the cost of your upgrade?',
        'sorting' : 6,
        'eligibility_clause' : """In ESS Clause 9.9.1 (e) the Accredited Certificate Provider has evidence satifactory to the Scheme Administrator that the Purchaser has paid for the implementation, assessment and other associated works carried out at the Site, a Net Amount of at least $1000 (excluding GST) for each item of End-User Equipment installed as part of an implementation using any of Activity Definitions F1.1, F1.2, F4 (Air Conditioners other than Multi-split or Ducted systems), F16 or F17. <br />
                                  In ESS Clause 9.9.1 (f) For Implementation of Activity Definition F4 using Multi-split or Ducted systems, the Purchaser must pay for the implementation, assessment and other associated works carried out at the Site, a Nett Amount of at least $3000 (excluding GST). <br />
                                  To calculate payments for F4 in clauses (e) and (f), the cooling capacity is rounded down to the nearest whole kW."""
    }


class HVAC2_residential_building(BaseVariable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the new End-User Equipment be installed in a residential building or small business site?',
        'sorting' : 7,
        'eligibility_clause' : """In PDRS HVAC2 Eligibility Requirements Clause 2 it states that for the purposes of clause 9.9.1(d), the new or replacement End-User Equipment must be installed in a Large Business Site and cannot be installed in a Residential Building or Small Business Site, unless the activity is the replacement of an existing air conditioner in a centralised system or in the common areas of a BCA Class 2 building."""
    }


class HVAC2_installed_centralised_system_common_area_BCA_Class2_building(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the installation be in a centralised system or common area in a BCA Class 2 building?',
        'sorting' : 8,
        'conditional': 'True',
        'eligibility_clause' : """In PDRS HVAC2 Eligibility Requirements Clause 2 it states that the New End-User Equipment or replacement End-User Equipment must not be installed in a Residential Building unless the activity is the replacement of an existing air conditioner in a centralised system or in the common areas of a Class 2 building."""
    }


class HVAC2_equipment_registered_in_GEMS(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the End-User Equipment be recorded in the GEMS Registry under an eligible product class?',
        'sorting' : 9,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 1 it states that the New End-User Equipment or replacement End-User Equipment must be recorded in the GEMS Registry under product classes 5-12, 18-21, 24-25 or 27 listed in the GEMS Registry as complying with either:
                                  a. Greenhouse and energy minimum standards (Air conditioners up to 65 kW) determination 2019; or
                                  b. Greenhouse and energy minimum standards (Air conditioners above 65 kW) determination 2022."""
    }


class HVAC2_model_number_registered_in_GEMS(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the model number(s) match those recorded in the GEMS Registry?',
        'sorting' : 10,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 5 it states that if the New End-User Equipment or replacement End-User Equipment is an eligible system for product classes 5-12 and 24-25, the model number(s) must match the model number(s) recorded in GEMS Registry."""
    }


class HVAC2_multi_split_product_class(BaseVariable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the End-User Equipment be an outdoor Multi-split?',
        'sorting' : 11,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 6 it states that if the new End-User Equipment or replacement End-User Equipment is an eligible outdoor Multi-split system under the GEMS Registry for Product Classes 18-21 and 27."""
    }


class HVAC2_outdoor_units(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will all indoor and outdoor units use the same manufacturer brand?',
        'sorting' : 12,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 6(b) it states that the manufacturer brand must be the same for all indoor and outdoor End-User Equipment."""
    }


class HVAC2_manufacture_approved_GEMS(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the End-User Equipment be a manufacturer approved combination with the outdoor unit matching the GEMS-registered model?',
        'sorting' : 13,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 6(a) it states that the outdoor unit part of the GEMS registered model number must match the model number of the outdoor unit being installed, <br />
                                  In PDRS HVAC2 Equipment Requirements Clause 6(c) it states that the unit(s) must be an approved combination by the manufacturer."""
    }


class HVAC2_new_equipment_cooling_capacity(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Will the End-User Equipment have a cooling capacity recorded in the GEMS registry?',
        'sorting' : 14,
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 2 it states that if the New End-User Equipment or replacement End-User Equipment has a Cooling Capacity recorded in the GEMS Registry"""
    }


class HVAC2_AEER_greater_than_minimum(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the Rated AEER equal to or greater than the minimum for the Product Class in Table F4.4?',
        'sorting' : 15,
        'conditional' : 'True',
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 2(b) it states that if it does not have a Commercial TCSPF_mixed value recorded in the GEMS Registry, then it must have a Rated AEER in the GEMS Registry equal to or greater than the Minimum Rated AEER for the same Product Class in Table F4.4."""
    }


class HVAC2_TCPSF_greater_than_minimum(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the Commercial TCSPF_mixed value equal to or greater than the minimum for the same Product Class in Table F4.4?',
        'sorting' : 16,
        'conditional' : 'True',
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 2(a) it states that it must have a Commercial TCSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial TCSPF_mixed value for the same Product Class in Table F4.4."""
    }


class DefaultValuesClimateZone(Enum):
    hot_zone = "Hot zone"
    average_zone = "Average zone"
    cold_zone = "Cold zone"


class HVAC2_climate_zone(BaseVariable):
    value_type = Enum
    entity = Building
    possible_values = DefaultValuesClimateZone
    default_value = DefaultValuesClimateZone.average_zone
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Which climate zone is the End-User Equipment installed in, as defined in ESS Table A27?',
        'sorting' : 17
    }


class HVAC2_new_equipment_heating_capacity(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the End-User equipment have a heating capacity recorded in the GEMS Registry?',
        'sorting' : 18,
        'eligibility_clause' : """In ESS F4 Equipment Requirements Clauses 3 and 4 it states that:<br />
        3. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry, and is installed in the hot or average zone as defined in Table A27: <br />
        a. It must have a Commercial HSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_mixed value for the same Product Class in Table F4.4; or<br />
        b. If it does not have a Commercial HSPF_mixed value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Class in Table F4.4.<br />
        4. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry and is installed in the cold zone as defined in Table A27:<br />
        a. It must have a Commercial HSPF_cold value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_cold value for the same Product Class in Table F4.4; or<br />
        b. If it does not have a Commercial HSPF_cold value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Class in Table F4.4.
        """
    }


class HVAC2_HSPF_mixed_eligible(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the Commercial HSPF_mixed value be equal to or greater than the minimum for the same Product Class in Table F4.4?',
        'sorting' : 19,
        'conditional': 'True',
        'eligibility_clause' : """In ESS F4 Equipment Requirements Clauses 3(a) it states that it must have a Commercial HSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_mixed value for the same Product Class in Table F4.4."""
    }


class HVAC2_ACOP_eligible(BaseVariable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    default_value = True
    metadata = {
        'display_question' : 'Will the Rated ACOP be equal to or greater than the minimum for the same Product Class in Table F4.4?',
        'sorting' : 20,
        'conditional': 'True',
        'eligibility_clause' : """In ESS F4 Equipment Requirements Clauses 3(b) it states that if it does not have a Commercial HSPF_mixed value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Class in Table F4.4."""
    }


class HVAC2_HSPF_cold_eligible(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the Commercial HSPF_cold value be equal to or greater than the minimum value for the same Product Class in Table F4.4?',
        'sorting' : 21,
        'conditional': 'True',
        'eligibility_clause' : """In ESS F4 Equipment Requirements Clauses 4(a) it states that it must have a Commercial HSPF_cold value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_cold value for the same Product Class in Table F4.4."""
    }


class HVAC2_ACOP_cold_eligible(BaseVariable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    default_value = True
    metadata = {
        'display_question' : 'Will the Rated ACOP be equal to or greater than the minimum for the same Product Class in Table F4.4?',
        'sorting' : 20,
        'conditional': 'True',
        'eligibility_clause' : """In ESS F4 Equipment Requirements Clauses 4(b) it states that if it does not have a Commercial HSPF_cold value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Class in Table F4.4."""
    }
