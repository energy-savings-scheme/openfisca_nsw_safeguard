from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class RF1_peak_demand_savings_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting',
        'alias': 'Peak demand savings capacity',
        'label': 'Peak demand savings capacity'
    }

    def formula(buildings, period, parameters):
      baseline_peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['baseline_peak_adjustment']['RF1']
      baseline_input_power = 0.093
      peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['peak_adjustment']['RF1']
      input_power = 0
      firmness_factor = 1

      peak_demand_savings_capacity= ((baseline_peak_adjustment_factor * baseline_input_power)
                                        - (input_power * peak_adjustment_factor )) * firmness_factor
      return peak_demand_savings_capacity
  
  
class RF1_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      peak_demand_savings_capacity = buildings('RF1_peak_demand_savings_capacity', period)
      summer_peak_demand_reduction_duration = 6
      lifetime = 7

      return peak_demand_savings_capacity * summer_peak_demand_reduction_duration * lifetime

  
class RF1_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'RF2 PRC calculation'
    metadata = {
        'variable-type': 'output'
    }
    
    def formula(buildings, period, parameters):
        peak_demand_reduction_capacity = buildings('RF1_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('RF1_network_loss_factor', period) 
        
        result = (peak_demand_reduction_capacity * network_loss_factor * 10)
        
        result_to_return = np.select([
                result <= 0, result > 0
            ], [
                0, result
            ])
        
        return result_to_return