from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


# From GEMS
class SYS2_input_power(Variable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Rated cooling input power (kW)'
    metadata = {
        'display_question' : 'Rated cooling input power at 35C as recorded in the GEMS registry',
        'sorting' : 9,
        'label': 'Rated cooling input power (kW)'
    }