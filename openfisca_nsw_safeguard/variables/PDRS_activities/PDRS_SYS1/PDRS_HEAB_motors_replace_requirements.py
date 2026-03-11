from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class PDRS_replace_motors_meets_implementation_requirements(BaseVariable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Implementation' \
            ' Requirements defined in PDRS replace or install high efficiency motors activity?'
    metadata = {
        'alias': "Replacement motor meets implementation requirements",
        "regulation_reference": PDRS_2022["HEAB", "motors_replace", "implementation"]}

    def formula(buildings, period, parameters):

        is_removed = buildings('Equipment_is_removed', period)
        performed_by_qualified_person = buildings(
            'Implementation_is_performed_by_qualified_person', period)
        return is_removed * performed_by_qualified_person


class PDRS_replace_motors_meets_all_requirements(BaseVariable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the' \
            ' Requirements defined in PDRS replace or install high efficiency motors activity?'
    metadata = {
        'alias': "Replacement motor meets all requirements",
    }

    def formula(buildings, period, parameters):
        implementation = buildings(
            'PDRS_replace_motors_meets_implementation_requirements', period)
        return implementation
