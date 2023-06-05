from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class D17_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        Baseline_A = buildings('D17_Baseline_A', period)
        a = 2.320
        Bs = buildings('D17_Bs', period)
        Be = buildings('D17_Be', period)

        electricity_savings = (Baseline_A - a) * (Bs + Be)
        return electricity_savings