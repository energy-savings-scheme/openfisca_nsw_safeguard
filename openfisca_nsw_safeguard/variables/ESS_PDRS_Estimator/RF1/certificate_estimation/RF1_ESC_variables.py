from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


""" Parameters for RF1 ESC Calculation
    These variables use Rule tables
"""
class RF1_PDRS__postcode(Variable):
    # this variable is used as the first input on all estimator certificate calculation pages
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = "What is the postcode for the building you are calculating PRCs for?"
    metadata={
        'variable-type' : 'user-input',
        'label': 'Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1
        }


class RF1_storage_volume(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label': 'Refrigerator or freezer storage capacity',
        'display_question' : 'Is the capacity of the non-primary refrigerator or freezer that is being removed 200 litres or greater?',
        'sorting' : 4
        }