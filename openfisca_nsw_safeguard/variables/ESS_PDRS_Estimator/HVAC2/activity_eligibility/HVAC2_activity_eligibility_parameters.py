import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class HVAC2_installation(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is the activity the installation of a new air conditioner?'
    metadata = {
        'display_question' : 'Is the activity the installation of a new air conditioner?',
        'sorting' : 1
    }


class HVAC2_equipment_replaced(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is the activity the replacement of an existing air conditioner?'
    metadata = {
        'display_question' : 'Is the activity the replacement of an existing air conditioner?',
        'sorting' : 2,
        'conditional': 'True'
    }


class HVAC2_equipment_removed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Has the removal of the existing equipment and the installation of the end-user equipment been performed or supervised by a suitably licensed person?'
    metadata = {
        'display_question' : 'Has the removal of the existing equipment and the installation of the end-user equipment been performed or supervised by a suitably licensed person?',
        'sorting' : 3, 
        'conditional': 'True'
    }


class HVAC2_Installed_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Has the installation of the end-user equipment been performed or supervised by a suitably licensed person?'
    metadata = {
        'display_question': 'Has the installation of the end-user equipment been performed or supervised by a suitably licensed person?',
        'sorting' : 4,
        'conditional': 'True'
    }


class HVAC2_Equipment_installed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is the new End-User equipment installed and operational?'
    metadata = {
        'display_question' : 'Is the new End-User equipment installed and operational?',
        'sorting' : 5
    }


class HVAC2_residential_building(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Has the new End-User equipment been installed in a residential building?'
    metadata = {
        'display_question' : 'Has the new End-User equipment been installed in a residential building?',
        'sorting' : 6
    }


class HVAC2_installed_centralised_system_common_area_BCA_Class2_building(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is the installation in a centralised system or common area in a Class 2 building?'
    metadata = {
        'display_question' : 'Is the installation in a centralised system or common area in a Class 2 building?',
        'sorting' : 7,
        'conditional': 'True'
    }


class HVAC2_equipment_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is the new air conditioner recorded in the GEMS registry (as defined within the GEMS Determination 2019)?'
    metadata = {
        'display_question' : 'Is the new air conditioner recorded in the GEMS registry (as defined within the GEMS Determination 2019)?',
        'sorting' : 8,
        'conditonal' : 'True'
    }


class HVAC2_new_equipment_cooling_capacity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Does the new air conditioner have a cooling capacity recorded in the GEMS registry?'
    metadata = {
        'display_question': 'Does the new air conditioner have a cooling capacity recorded in the GEMS registry?',
        'sorting' : 9
    }


class HVAC2_AEER_greater_than_minimum(Variable):
    value_type = bool
    entity = Building
    default_value = True
    label = 'Is your AEER equal to or greater than the Minimum for the same Product Type and Cooling Capacity?'
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is your AEER equal to or greater than the Minimum AEER for the same Product Type and Cooling Capacity in ESS Table F4.4?',
        'sorting' : 10,
        'conditonal' : 'True'
    }


class HVAC2_TCPSF_greater_than_minimum(Variable):
    value_type = bool
    entity = Building
    default_value = True
    label = 'Is your TCPSF equal to or greater than the Minimum TCPSF for the same Product Type and Cooling Capacity in ESS Table F4.5?'
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is your TCPSF equal to or greater than the Minimum TCPSF for the same Product Type and Cooling Capacity in ESS Table F4.5?',
        'sorting' : 11,
        'conditional': 'True'
    }


class DefaultValuesClimateZone(Enum):
    hot_zone = "AC is installed in the hot zone."
    average_zone = "AC is installed in the average zone."
    cold_zone = "AC is installed in the cold zone."


class HVAC2_climate_zone(Variable):
    value_type = Enum
    entity = Building
    label = "Which climate zone is the End-User equipment installed in, as defined in ESS Table A27?"
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
        'sorting' : 13
    }


class HVAC2_HSPF_mixed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is your GEMS Commercial HSPF_mixed value equal to or greater than the Minimum Commercial HSPF_mixed value for the same Product Type and Cooling Capacity in ESS Table F4.4?'
    metadata = {
        'display_question' : 'Is your GEMS Commercial HSPF_mixed value equal to or greater than the Minimum Commercial HSPF_mixed value for the same Product Type and Cooling Capacity i,n ESS Table F4.4?',
        'sorting' : 14,
        'conditional': 'True'
    }


class HVAC2_ACOP(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    default_value = True
    label = 'Is your ACOP equal to or greater than the Minimum ACOP for the same Product Type and Cooling Capacity in ESS Table F4.5?'
    metadata = {
        'display_question' : 'Is your ACOP equal to or greater than the Minimum ACOP for the same Product Type and Cooling Capacity in ESS Table F4.5?',
        'sorting' : 15,
        'conditional': 'True'
    }


class HVAC2_HSPF_cold(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is your GEMS Commercial HSPF_cold value equal to or greater than the Minimum Commercial HSPF_cold value for the same Product Type and Cooling Capacity in ESS Table F4.4?'
    metadata = {
        'display_question' : 'Is your GEMS Commercial HSPF_cold value equal to or greater than the Minimum Commercial HSPF_cold value for the same Product Type and Cooling Capacity in ESS Table F4.4?',
        'sorting' : 16,
        'conditional': 'True'
    }