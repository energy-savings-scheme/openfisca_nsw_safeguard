from decimal import FloatOperation
import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class SYS1_temperature_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        # user input
        temp_factor = buildings('SYS1_temperature_factor', period)
        usage_factor = 0.6

        baseline_input_power = temp_factor * usage_factor
        return baseline_input_power

