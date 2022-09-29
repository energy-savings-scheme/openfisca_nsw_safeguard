import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS_HEER_AC_replace_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the equipment meet all of the Eligibility' \
            ' Requirements defined in installing a high efficiency air conditioner for Residential?'
    metadata = {
        'alias': "HEER AC Install meets eligibility requirements",
    }


class ESS_HEER_AC_replace_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the equipment meet all of the Equipment' \
            ' Requirements defined in replacing a high efficiency air conditioner for Residential?'
    metadata = {
        'alias': "HEER AC replace meets equipment requirements",
    }

    def formula(buildings, period, parameters):
        is_in_GEMS = buildings(
            'Appliance_is_registered_in_GEMS', period)
        cooling_capacity = buildings('new_AC_cooling_capacity', period)
        has_cooling_capacity = (
                                (cooling_capacity != 0) *
                                (cooling_capacity != None)
                                )
        TCSPF_or_AEER_exceeds_benchmark = buildings(
            'AC_TCSPF_or_AEER_exceeds_ESS_benchmark', period) 
            # note that logic relating to whether to use TCSPF or AEER
            # is contained in the above variable for clarity
        heating_capacity = buildings('new_AC_heating_capacity', period)
        has_heating_capacity = (
                                (heating_capacity != 0) *
                                (heating_capacity != None)
                                )
        HSPF_or_ACOP_exceeds_benchmark = buildings(
            'AC_HSPF_or_ACOP_exceeds_ESS_benchmark', period)
            # note that logic relating to whether to use HSPF or ACOP
            # and whether it is installed in 
            # is contained in the above variable for clarity

        return (
                is_in_GEMS * 
                (
                (
                    (has_cooling_capacity * TCSPF_or_AEER_exceeds_benchmark) +
                    np.logical_not(has_cooling_capacity) 
                ) *
                    (has_heating_capacity * HSPF_or_ACOP_exceeds_benchmark) +
                    np.logical_not(has_heating_capacity) 
                )
                )


class ESS_HEER_AC_replace_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Implementation' \
            ' Requirements defined in replacing a high efficiency air conditioner for Residential?'
    metadata = {
        'alias': "HEER AC replace meets implementation requirements",
    }

    def formula(buildings, period, parameters):
        is_installed = buildings(
            'Equipment_is_installed', period)
        is_removed = buildings("Equipment_is_removed", period)
        performed_by_qualified_person = buildings(
            'Implementation_is_performed_by_qualified_person', period)

        return is_installed * is_removed * performed_by_qualified_person


class ESS_HEER_AC_replace_meets_all_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the' \
            ' Requirements defined in replacing a high efficiency air conditioner for Residential?'
    metadata = {
        'alias': "HEER AC replace meets all requirements",
    }

    def formula(buildings, period, parameters):
        eligibility = buildings(
            'ESS_HEER_AC_replace_meets_eligibility_requirements', period)
        equipment = buildings(
            'ESS_HEER_AC_replace_meets_equipment_requirements', period)
        implementation = buildings(
            'ESS_HEER_AC_replace_meets_implementation_requirements', period)

        return implementation * eligibility * equipment
