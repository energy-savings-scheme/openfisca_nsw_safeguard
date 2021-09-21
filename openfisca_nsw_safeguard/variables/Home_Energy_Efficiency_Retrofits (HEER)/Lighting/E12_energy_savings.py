from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class E12_deemed_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    default_value = 0.91
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        energy_savings = 0.91
        return energy_savings
