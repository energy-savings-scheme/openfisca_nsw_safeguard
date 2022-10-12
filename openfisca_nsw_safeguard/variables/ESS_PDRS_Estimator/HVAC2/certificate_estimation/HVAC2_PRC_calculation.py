from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class HVAC2_baseline_input_power(Variable):
    """ Note that baseline input power is the same value as input power
    """
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Baseline input'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      rated_cooling_capacity = buildings('HVAC2_cooling_capacity_input', period)
      baseline_AEER = buildings('HVAC2_baseline_AEER_input', period)

      baseline_input_power = rated_cooling_capacity / baseline_AEER
      return baseline_input_power


class HVAC2_baseline_peak_adjustment_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HVAC2 baseline peak adjustment factor'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      usage_factor = 0.6
      climate_zone = buildings('BCA_climate_zone', period)
      temperature_factor = parameters(period).PDRS.table_A28_temperature_factor.temperature_factor[climate_zone]

      baseline_adjustment_factor = usage_factor * temperature_factor
      return baseline_adjustment_factor


class HVAC2_peak_demand_savings_activity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand savings activity'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        baseline_input_power = buildings('HVAC2_baseline_input_power', period)
        baseline_peak_adjustment = buildings('HVAC2_baseline_peak_adjustment_factor', period)
        input_power = buildings('HVAC2_input_power', period)
        peak_adjustment_factor = buildings('HVAC2_baseline_peak_adjustment_factor', period)
        firmness_factor = 1

        peak_demand_savings_activity = np.floor((baseline_input_power * baseline_peak_adjustment)-(input_power * peak_adjustment_factor)) * firmness_factor
        return peak_demand_savings_activity

  
class HVAC2_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand reduction capacity'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        peak_demand_savings = buildings('HVAC2_peak_demand_savings_activity', period)
        summer_peak_demand_duration = 6
        lifetime = buildings('HVAC2_lifetime_value', period)

        peak_demand_reduction_capacity = (peak_demand_savings * summer_peak_demand_duration * lifetime)
        return peak_demand_reduction_capacity


class HVAC2_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of PRCs for HVAC2'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        peak_demand_capacity = buildings('HVAC2_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('HVAC2_network_loss_factor', period)
        kw_to_0_1kw = 10


        HVAC2_PRC_calculation = np.floor(peak_demand_capacity * network_loss_factor) * kw_to_0_1kw        
        return HVAC2_PRC_calculation
