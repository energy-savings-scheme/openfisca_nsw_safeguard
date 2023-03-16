import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class SYS2_peak_demand_savings_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
      'variable-type' : 'inter-interesting',
      'label' : 'Peak Demand Savings Capacity'
    }

    def formula(buildings, period, parameters):
        baseline_input_power = buildings('SYS2_baseline_input_power', period)
        baseline_peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['baseline_peak_adjustment']['SYS2']
        input_power = buildings('SYS2_input_power', period)
        peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['peak_adjustment']['SYS2']
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor['firmness_factor']['SYS2']

        peak_demand_savings_capacity = ((baseline_input_power * baseline_peak_adjustment_factor) - (input_power * peak_adjustment_factor)) * firmness_factor

        return peak_demand_savings_capacity


class SYS2_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand reduction capacity'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        peak_demand_savings = buildings('SYS2_peak_demand_savings_capacity', period)
        summer_peak_demand_duration = 6
        lifetime = 12

        peak_demand_reduction_capacity = (peak_demand_savings * summer_peak_demand_duration * lifetime)
        return peak_demand_reduction_capacity


class SYS2_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'label' : 'The number of PRCs for SYS2',
        'variable-type' : 'output'
    }

    def formula(buildings, period, parameters):
        peak_demand_capacity = buildings('SYS2_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('SYS2_get_network_loss_factor_by_postcode', period)
        kw_to_0_1kw = 10
        replacement_activity = buildings('SYS2_replacement_activity', period)

        SYS2_eligible_PRCs = np.select(
            [
                replacement_activity,
                np.logical_not(replacement_activity)
            ],
            [
                (peak_demand_capacity * network_loss_factor * kw_to_0_1kw),
                0
            ])

        result_to_return = np.select(
            [
                SYS2_eligible_PRCs <= 0, SYS2_eligible_PRCs > 0
            ],
            [
                0, SYS2_eligible_PRCs
            ])
        return result_to_return