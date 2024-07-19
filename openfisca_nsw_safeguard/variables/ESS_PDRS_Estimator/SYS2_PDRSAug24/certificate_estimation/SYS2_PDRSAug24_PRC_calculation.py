import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class SYS2_PDRSAug24_peak_demand_savings_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
      'variable-type' : 'inter-interesting',
      'label' : 'Peak Demand Savings Capacity'
    }

    def formula(buildings, period, parameters):
        baseline_input_power = buildings('SYS2_PDRSAug24_baseline_input_power', period)
        baseline_peak_adjustment_factor = parameters(period).PDRS.table_A4_PDRSAug24_adjustment_factors['baseline_peak_adjustment']['SYS2']
        input_power = buildings('SYS2_PDRSAug24_input_power', period)
        peak_adjustment_factor = parameters(period).PDRS.table_A4_PDRSAug24_adjustment_factors['peak_adjustment']['SYS2']
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor['firmness_factor']['SYS2']

        peak_demand_savings_capacity = ((baseline_input_power * baseline_peak_adjustment_factor) - (input_power * peak_adjustment_factor)) * firmness_factor

        return peak_demand_savings_capacity
    

class SYS2_PDRSAug24_peak_demand_annual_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand annual savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #Projected annual energy consumption
        PAEC = buildings('SYS2_PDRSAug24_projected_annual_energy_consumption', period)

        #Daily run time
        DRT = buildings('SYS2_PDRSAug24_daily_run_time', period)

        #input power
        input_power = PAEC / (365 * DRT)

        #nameplate input power
        nameplate_input_power = buildings('SYS2_PDRSAug24_nameplate_input_power', period)

        nameplate_input_power_to_check = np.select(
            [
                (nameplate_input_power <= 1000),
                (nameplate_input_power > 1000) * (nameplate_input_power <= 1500),
                (nameplate_input_power > 1500) * (nameplate_input_power <= 2000),
                (nameplate_input_power > 2000),
            ],
            [
                'less_than_or_equal_to_1000w',
                '1001_to_1500w',
                '1501_to_2000w',
                'greater_than_2000w'
            ])

        #baseline input power
        baseline_input_power = parameters(period).PDRS.pool_pumps.table_sys2_1_PDRSAug24['baseline_input_power'][nameplate_input_power_to_check]

        #baseline peak adjustment factor
        baseline_peak_adjustment_factor = parameters(period).PDRS.table_A4_PDRSAug24_adjustment_factors['baseline_peak_adjustment']['SYS2']

        #peak adjustment factor
        peak_adjustment_factor = parameters(period).PDRS.table_A4_PDRSAug24_adjustment_factors['peak_adjustment']['SYS2']

        #firmness factor
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor['firmness_factor']['SYS2']

        #peak demand savings capacity
        peak_demand_savings_capacity = ((baseline_input_power * baseline_peak_adjustment_factor) - (input_power * peak_adjustment_factor)) * firmness_factor

        #peak demand annual savings 
        summer_peak_demand_reduction_duration = 6   
        lifetime = 10

        peak_demand_annual_savings = peak_demand_savings_capacity * summer_peak_demand_reduction_duration * lifetime
        
        peak_demand_annual_savings_return = np.select([
                peak_demand_annual_savings <= 0, peak_demand_annual_savings > 0
            ],
	        [
                0, peak_demand_annual_savings
            ])
        
        return peak_demand_annual_savings_return        


class SYS2_PDRSAug24_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand reduction capacity'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        peak_demand_savings = buildings('SYS2_PDRSAug24_peak_demand_savings_capacity', period)
        summer_peak_demand_duration = 6
        lifetime = 10

        peak_demand_reduction_capacity = (peak_demand_savings * summer_peak_demand_duration * lifetime)
        return peak_demand_reduction_capacity


class SYS2_PDRSAug24_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'label' : 'The number of PRCs for SYS2',
        'variable-type' : 'output'
    }

    def formula(buildings, period, parameters):
        peak_demand_capacity = buildings('SYS2_PDRSAug24_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('SYS2_PDRSAug24_get_network_loss_factor_by_postcode', period)
        kw_to_0_1kw = 10

        result = (peak_demand_capacity * network_loss_factor * kw_to_0_1kw)
                

        result_to_return = np.select([
                result <= 0, 
                result > 0
        ],
        [
                0, 
                result
        ])
        
        return result_to_return