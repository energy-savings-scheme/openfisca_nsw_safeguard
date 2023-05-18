import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class HVAC2NewInstallationReplacement(Enum):
    new_installation_activity = 'Installation of a new air conditioner'
    replacement_activity = 'Replacement of an existing air conditioner'


class HVAC2_new_installation_or_replacement(Variable):
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


class HVAC2_new_installation_or_replacement_eligible(Variable):
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


class HVAC2_installed_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Has the removal of the existing equipment and the installation of the end-user equipment been performed or supervised by a suitably licensed person?',
        'sorting' : 4,
        'conditional': 'True',
        'eligibility_clause' : """In PDRS HVAC2 Implementation Requirements Clause 3 it states that the activity, including the removal of any existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class HVAC2_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Was or will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 5,
        'eligibility_clause' : """In ESS Clause 6.2 it states that an Accredited Certificate Provider may only create Energy Savings Certificates in respect of the Energy Savings for an Implementation where:<br />
                                  (a) the Accredited Certificate Provider is the Energy Saver for those Energy Savings as at the Implementation Date; and <br />
                                  (b) the Accredited Certificate Provider’s Accreditation Date for that Recognised Energy Saving Activity is prior to the Implementation Date."""
    }


class HVAC2_residential_building(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the new End-User equipment been installed in a residential building?',
        'sorting' : 6,
        'eligibility_clause' : """In PDRS HVAC2 Eligibility Requirements Clause 2 it states that the New End-User Equipment or replacement End-User Equipment must not be installed in a Residential Building unless the activity is the replacement of an existing air conditioner in a centralised system or in the common areas of a Class 2 building."""
    }


class HVAC2_installed_centralised_system_common_area_BCA_Class2_building(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the installation in a centralised system or common area in a Class 2 building?',
        'sorting' : 7,
        'conditional': 'True',
        'eligibility_clause' : """In PDRS HVAC2 Eligibility Requirements Clause 2 it states that the New End-User Equipment or replacement End-User Equipment must not be installed in a Residential Building unless the activity is the replacement of an existing air conditioner in a centralised system or in the common areas of a Class 2 building."""
    }


class HVAC2_equipment_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the new air conditioner recorded in the GEMS registry (as defined within the GEMS Determination 2019)?',
        'sorting' : 8,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 1 it states that the New End-User Equipment or replacement End-User Equipment must be a registered product in the GEMS Registry as complying with the Greenhouse and Energy Minimum Standards (Air Conditioners up to 65kW) Determination 2019.  """
    }


class HVAC2_new_equipment_cooling_capacity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Does the new air conditioner have a cooling capacity recorded in the GEMS registry?',
        'sorting' : 9,
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 2 it states that if the New End-User Equipment or replacement End-User Equipment has a Cooling Capacity recorded in the GEMS Registry: <br />
        a. The New End-User Equipment or replacement End-User Equipment must have a Commercial TCSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial TCSPF_mixed value for the corresponding Product Type and Cooling Capacity in Table HVAC2.3; or <br />
        b. If the New End-User Equipment or replacement End-User Equipment does not have a Commercial TCSPF_mixed value recorded in the GEMS Registry, then it must have an AEER in the GEMS Registry equal to or greater than the Minimum AEER for the Product Type and Cooling Capacity in Table HVAC2.4."""
    }


class HVAC2_AEER_greater_than_minimum(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is your AEER equal to or greater than the Minimum AEER for the Product Type and Cooling Capacity in PDRS Table HVAC2.4?',
        'sorting' : 10,
        'conditional' : 'True',
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 2 it states that if the New End-User Equipment or replacement End-User Equipment has a Cooling Capacity recorded in the GEMS Registry: <br />
        a. The New End-User Equipment or replacement End-User Equipment must have a Commercial TCSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial TCSPF_mixed value for the corresponding Product Type and Cooling Capacity in Table HVAC2.3; or <br />
        b. If the New End-User Equipment or replacement End-User Equipment does not have a Commercial TCSPF_mixed value recorded in the GEMS Registry, then it must have an AEER in the GEMS Registry equal to or greater than the Minimum AEER for the Product Type and Cooling Capacity in Table HVAC2.4."""
    }


class HVAC2_TCPSF_greater_than_minimum(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is your Commercial TCSPF_mixed value equal to or greater than the Minimum Commercial TCPSF_mixed value for the same Product Type and Cooling Capacity in Table PDRS HVAC2.3?',
        'sorting' : 11,
        'conditional' : 'True',
        'eligibility_clause' : """In PDRS HVAC2 Equipment Requirements Clause 2 it states that if the New End-User Equipment or replacement End-User Equipment has a Cooling Capacity recorded in the GEMS Registry: <br />
        a. The New End-User Equipment or replacement End-User Equipment must have a Commercial TCSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial TCSPF_mixed value for the corresponding Product Type and Cooling Capacity in Table HVAC2.3; or <br />
        b. If the New End-User Equipment or replacement End-User Equipment does not have a Commercial TCSPF_mixed value recorded in the GEMS Registry, then it must have an AEER in the GEMS Registry equal to or greater than the Minimum AEER for the Product Type and Cooling Capacity in Table HVAC2.4."""
    }


class DefaultValuesClimateZone(Enum):
    hot_zone = "Hot zone"
    average_zone = "Average zone"
    cold_zone = "Cold zone"


class HVAC2_climate_zone(Variable):
    value_type = Enum
    entity = Building
    possible_values = DefaultValuesClimateZone
    default_value = DefaultValuesClimateZone.average_zone
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Which climate zone is the End-User equipment installed in, as defined in ESS Table A27?',
        'sorting' : 12
    }


class HVAC2_new_equipment_heating_capacity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Does the new or replacement End-User equipment have a heating capacity recorded in the GEMS Registry?'
    metadata = {
        'display_question' : 'Does the new or replacement End-User equipment have a heating capacity recorded in the GEMS Registry?',
        'sorting' : 13,
        'eligibility_clause' : """In ESS F4 Equipment Requirements Clauses 3 and 4 it states that:<br />
        3. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry, and is installed in the hot or average zone as defined in Table A27: <br />
        a. It must have a Commercial HSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_mixed value for the same Product Type and Cooling Capacity in Table F4.4; or<br />
        b. If it does not have a Commercial HSPF_mixed value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table F4.5.<br />
        4. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry and is installed in the cold zone as defined in Table A27:<br />
        a. It must have a Commercial HSPF_cold value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_cold value for the same Product Type and Cooling Capacity in Table F4.4; or<br />
        b. If it does not have a Commercial HSPF_cold value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table F4.5.
        """
    }


class HVAC2_HSPF_mixed_eligible(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is your GEMS Commercial HSPF_mixed value equal to or greater than the Minimum Commercial HSPF_mixed value for the same Product Type and Cooling Capacity in ESS Table F4.4?'
    metadata = {
        'display_question' : 'Is your GEMS Commercial HSPF_mixed value equal to or greater than the Minimum Commercial HSPF_mixed value for the same Product Type and Cooling Capacity in ESS Table F4.4?',
        'sorting' : 14,
        'conditional': 'True',
        'eligibility_clause' : """In ESS F4 Equipment Requirements Clauses 3 and 4 it states that:<br />
        3. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry, and is installed in the hot or average zone as defined in Table A27: <br />
        a. It must have a Commercial HSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_mixed value for the same Product Type and Cooling Capacity in Table F4.4; or<br />
        b. If it does not have a Commercial HSPF_mixed value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table F4.5.<br />
        4. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry and is installed in the cold zone as defined in Table A27:<br />
        a. It must have a Commercial HSPF_cold value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_cold value for the same Product Type and Cooling Capacity in Table F4.4; or<br />
        b. If it does not have a Commercial HSPF_cold value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table F4.5.
        """
    }


class HVAC2_ACOP_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    default_value = True
    label = 'Is your ACOP equal to or greater than the Minimum ACOP for the same Product Type and Cooling Capacity in ESS Table F4.5?'
    metadata = {
        'display_question' : 'Is your ACOP equal to or greater than the Minimum ACOP for the same Product Type and Cooling Capacity in ESS Table F4.5?',
        'sorting' : 15,
        'conditional': 'True',
        'eligibility_clause' : """In ESS F4 Equipment Requirements Clauses 3 and 4 it states that:<br />
        3. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry, and is installed in the hot or average zone as defined in Table A27: <br />
        a. It must have a Commercial HSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_mixed value for the same Product Type and Cooling Capacity in Table F4.4; or<br />
        b. If it does not have a Commercial HSPF_mixed value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table F4.5.<br />
        4. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry and is installed in the cold zone as defined in Table A27:<br />
        a. It must have a Commercial HSPF_cold value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_cold value for the same Product Type and Cooling Capacity in Table F4.4; or<br />
        b. If it does not have a Commercial HSPF_cold value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table F4.5.
        """
    }


class HVAC2_HSPF_cold_eligible(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is your GEMS Commercial HSPF_cold value equal to or greater than the Minimum Commercial HSPF_cold value for the same Product Type and Cooling Capacity in ESS Table F4.4?'
    metadata = {
        'display_question' : 'Is your GEMS Commercial HSPF_cold value equal to or greater than the Minimum Commercial HSPF_cold value for the same Product Type and Cooling Capacity in ESS Table F4.4?',
        'sorting' : 16,
        'conditional': 'True',
        'eligibility_clause' : """In ESS F4 Equipment Requirements Clauses 3 and 4 it states that:<br />
        3. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry, and is installed in the hot or average zone as defined in Table A27: <br />
        a. It must have a Commercial HSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_mixed value for the same Product Type and Cooling Capacity in Table F4.4; or<br />
        b. If it does not have a Commercial HSPF_mixed value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table F4.5.<br />
        4. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry and is installed in the cold zone as defined in Table A27:<br />
        a. It must have a Commercial HSPF_cold value, as recorded in the GEMS Registry, equal to or greater than the Minimum Commercial HSPF_cold value for the same Product Type and Cooling Capacity in Table F4.4; or<br />
        b. If it does not have a Commercial HSPF_cold value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table F4.5.
        """
    }