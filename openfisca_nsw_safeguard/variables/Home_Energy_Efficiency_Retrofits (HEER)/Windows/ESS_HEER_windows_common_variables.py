from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

class ESS_HEER_window_or_door_U_value(Variable):
    value_type = float  # note need to recode as Enum once reading AS2040
    entity = Building
    definition_period = ETERNITY
    label = 'What is the system U-Value for the thermally efficient window' \
            ' or door?'
