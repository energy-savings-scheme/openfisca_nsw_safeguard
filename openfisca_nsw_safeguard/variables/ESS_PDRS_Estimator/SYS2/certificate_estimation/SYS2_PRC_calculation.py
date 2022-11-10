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
