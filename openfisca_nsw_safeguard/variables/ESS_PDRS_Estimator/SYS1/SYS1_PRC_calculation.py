from xml.etree import ElementInclude
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class SYS1_baseline_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Baseline input power (kW)'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        # user input
        SYS1_new_equipment_rated_output = buildings('SYS1_new_equipment_rated_output', period)
        SYS1_baseline_efficiency = buildings('SYS1_baseline_efficiency', period)

        baseline_input_power = np.multiply(SYS1_new_equipment_rated_output, (SYS1_baseline_efficiency/100))
        return baseline_input_power
    
    
class SYS1_baseline_peak_adjustment_factor(Variable):
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


