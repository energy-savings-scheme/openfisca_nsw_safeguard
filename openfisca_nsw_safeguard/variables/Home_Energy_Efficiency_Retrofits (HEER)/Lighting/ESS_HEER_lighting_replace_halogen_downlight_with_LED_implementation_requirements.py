from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_lighting_replace_halogen_downlight_is_installed_by_authorised_person(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the activity was performed by a person authorised' \
            ' to carry out electrical wiring work, defined under section 14' \
            ' (1) of the Home Building Act 1989.'
