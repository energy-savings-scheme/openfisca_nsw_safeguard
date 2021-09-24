from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_HEER_new_product_warranty_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the warranty length of the new product, in years.'
