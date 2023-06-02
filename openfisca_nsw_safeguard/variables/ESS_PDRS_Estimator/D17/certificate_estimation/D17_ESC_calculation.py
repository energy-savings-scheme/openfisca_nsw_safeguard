from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class D17_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata={
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        Baseline_A = buildings('D17_Baseline_A', period)
        adjustment_coefficient = 2.320
        baseline_energy_consumption = buildings('D17_Bs', period)
        annual_electricity_usage = buildings('D17_Be', period)

        deemed_electricity_savings = (Baseline_A - adjustment_coefficient * (baseline_energy_consumption + annual_electricity_usage))
        return deemed_electricity_savings