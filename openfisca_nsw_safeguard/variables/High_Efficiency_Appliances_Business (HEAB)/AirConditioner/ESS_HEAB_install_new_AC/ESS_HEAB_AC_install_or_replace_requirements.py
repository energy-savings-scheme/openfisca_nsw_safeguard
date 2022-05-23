import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022
from openfisca_nsw_safeguard.variables.ESS_general.ESS_BCA_climate_zone import BCA_building_class

import numpy as np
from openfisca_nsw_safeguard.variables.PDRS_general.PDRS_number_of_certificates import PDRS_activity_type

class ESS_HEAB_AC_install_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Eligibility' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC install meets eligibility requirements",
        "regulation_reference": PDRS_2022["HEAB", "AC_install", "eligibility"]
    }

    def formula(buildings, period, parameters):
        activity_type = buildings('PDRS_activity_type', period)
        ActivityType = activity_type.possible_values
        is_install_AC = (activity_type == ActivityType.install_AC)
        is_replace_AC = (activity_type == ActivityType.replace_AC)
        BuildingClass = BCA_building_class.possible_values
        is_residential = (
                            (BCA_building_class == BuildingClass.BCA_Class_1a) +
                            (BCA_building_class == BuildingClass.BCA_Class_1b) +
                            (BCA_building_class == BuildingClass.BCA_Class_2) +
                            (BCA_building_class == BuildingClass.BCA_Class_4)
        )
        return (
            (is_install_AC + is_replace_AC) *
            np.logical_not(is_residential)
        )


class ESS_HEAB_AC_install_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the equipment meet all of the Equipment' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC Install meets equipment requirements",
        "regulation_reference": PDRS_2022["HEAB", "AC_install", "equipment"]
    }

    def formula(buildings, period, parameters):
        is_in_GEMS = buildings(
            'Appliance_is_registered_in_GEMS', period)

        TCSPF_or_AEER_exceeds_benchmark = buildings('AC_TCSPF_or_AEER_exceeds_ESS_benchmark', period)
        HSPF_or_ACOP_exceeds_benchmark = buildings('AC_HSPF_or_ACOP_exceeds_ESS_benchmark', period)

        return(
            is_in_GEMS *
            TCSPF_or_AEER_exceeds_benchmark * 
            HSPF_or_ACOP_exceeds_benchmark
        )        


class ESS_HEAB_AC_install_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Implementation' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC Install meets implementation requirements",
        "regulation_reference": PDRS_2022["HEAB", "AC_install", "implementation"]
    }

    def formula(buildings, period, parameters):
        is_installed = buildings(
            'Equipment_is_installed', period)
        performed_by_qualified_person = buildings(
            'implementation_is_performed_by_qualified_person', period)

        return (
                is_installed * 
                performed_by_qualified_person
                )


class ESS_HEAB_residential_AC_install_meets_all_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC install meets all requirements",
    }

    def formula(buildings, period):
        eligibility = buildings(
            'ESS_HEAB_residential_AC_install_meets_eligibility_requirements', period)
        equipment = buildings(
            'ESS_HEAB_residential_AC_install_meets_equipment_requirements', period)
        implementation = buildings(
            'ESS_HEAB_residential_AC_install_meets_implementation_requirements', period)

        return implementation * eligibility * equipment
