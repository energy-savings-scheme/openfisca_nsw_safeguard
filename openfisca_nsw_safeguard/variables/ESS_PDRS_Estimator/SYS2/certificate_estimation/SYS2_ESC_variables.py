import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for SYS2 ESC Calculation
    These variables use Rule tables
"""
class SYS2_PDRS__postcode(Variable):
    # using to get the regional network factor
    # this variable is used as the first input on all estimator certificate calculation pages
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'alias' : 'PDRS Postcode',
        'label': 'Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1
        }


class SYS2_replacement_activity(Variable):
    value_type = bool
    default_value = True
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'user-input',
        'label': 'Replacement or new installation activity',
        'display_question': 'Is the activity a replacement of existing equipment?',
        'sorting' : 3
    }