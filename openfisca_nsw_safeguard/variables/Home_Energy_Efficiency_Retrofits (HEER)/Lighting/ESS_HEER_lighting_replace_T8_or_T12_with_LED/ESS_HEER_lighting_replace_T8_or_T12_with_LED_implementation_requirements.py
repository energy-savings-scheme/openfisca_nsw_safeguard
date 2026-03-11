from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building


class ESS_HEER_lighting_replace_T8_or_T12_with_LED_is_installed_by_authorised_person(BaseVariable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the activity was performed by a person authorised' \
            ' to carry out electrical wiring work, defined under section 14' \
            ' (1) of the Home Building Act 1989.'


class ESS_HEER_lighting_replace_T8_or_T12_with_LED_meets_implementation_requirements(BaseVariable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the implementation meets the Implementation Requirements' \
            ' detailed in Activity Definition E5.'
