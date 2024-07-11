from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class RF1_peak_demand_annual_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand annual savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #peak demand savings capacity
        baseline_peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['baseline_peak_adjustment']['RF1']
        baseline_input_power = 0.093
        peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['peak_adjustment']['RF1']
        input_power = 0
        firmness_factor = 1

        temp1 = (baseline_peak_adjustment_factor * baseline_input_power)
        temp2 = (input_power * peak_adjustment_factor )
        
        peak_demand_savings_capacity = ((temp1 - temp2) * firmness_factor)

        #peak demand annual savings
        summer_peak_demand_reduction_duration = 6
        number_of_fridges = buildings('RF1_number_of_refrigerator_freezers_removal', period)
        lifetime = 7

        peak_demand_annual_savings = peak_demand_savings_capacity * summer_peak_demand_reduction_duration * number_of_fridges * lifetime
    
        peak_demand_annual_savings_return = np.select([
                peak_demand_annual_savings <= 0, peak_demand_annual_savings > 0
            ], 
	        [
                0, peak_demand_annual_savings
            ])
        
        return peak_demand_annual_savings_return

  
class RF1_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'RF1 PRC calculation'
    metadata = {
        'variable-type': 'output'
    }
    
    def formula(buildings, period, parameters):
        peak_demand_reduction_capacity = buildings('RF1_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('RF1_get_network_loss_factor_by_postcode', period) 
        storage_volume_eligibility = buildings('RF1_storage_volume', period)
        number_of_fridges = buildings('RF1_number_of_refrigerator_freezers_removal', period)

        RF1_eligible_PRCs = np.select(
        [
            storage_volume_eligibility,
            np.logical_not(storage_volume_eligibility)
        ],
        [
            (peak_demand_reduction_capacity * network_loss_factor * 10 * number_of_fridges),
            0
        ])

        result_to_return = np.select(
        [
            RF1_eligible_PRCs <= 0, RF1_eligible_PRCs > 0
        ],
        [
            0, RF1_eligible_PRCs
        ])
        return result_to_return