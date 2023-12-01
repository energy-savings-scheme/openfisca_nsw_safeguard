from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class BESS1_demand_shifting_component(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Demand shifting component'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        usable_battery_capacity = buildings('BESS1_usable_battery_capacity', period)
        demand_reduction_factor = 0.0853

        demand_shifting_component = usable_battery_capacity * demand_reduction_factor
        return demand_shifting_component