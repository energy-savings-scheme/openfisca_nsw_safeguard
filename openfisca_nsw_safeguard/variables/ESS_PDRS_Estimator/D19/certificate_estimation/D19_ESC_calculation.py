from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class D19_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        Baseline_A = buildings('D19_Baseline_A', period)
        a = 2.320
        Bs = buildings('D19_Bs', period)
        Be = buildings('D19_Be', period)

        electricity_savings = (Baseline_A - a) * (Bs + Be)
        return electricity_savings


class D19_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        deemed_activity_electricity_savings = buildings('D19_deemed_activity_electricity_savings', period)
        regional_network_factor = buildings('D19_regional_network_factor', period)

        electricity_savings = deemed_activity_electricity_savings * regional_network_factor
        return electricity_savings


class D19_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'output',
        'label' : 'The number of ESCs for D19'
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('D19_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        gas_savings = buildings('D19_Baseline_B', period)
        gas_certificate_conversion_factor = 0.39
        replacement_activity = buildings('D19_replacement_activity', period)

        D19_eligible_ESCs = np.select(
            [
                replacement_activity,
                np.logical_not(replacement_activity)
            ],
            [
                ((electricity_savings * electricity_certificate_conversion_factor) + (gas_savings * gas_certificate_conversion_factor)),
                0
            ])

        result_to_return = np.select(
            [
                D19_eligible_ESCs <= 0, D19_eligible_ESCs > 0
            ],
            [
                0, D19_eligible_ESCs
            ])
        return result_to_return