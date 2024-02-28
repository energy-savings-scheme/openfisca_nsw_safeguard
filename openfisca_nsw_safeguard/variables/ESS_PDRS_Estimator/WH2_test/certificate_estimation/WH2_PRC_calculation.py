from xml.etree import ElementInclude
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class WH2_test_baseline_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Baseline input power (kW)'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        # user input
        com_peak_load = buildings('WH2_test_com_peak_load', period)

        baseline_input_power = com_peak_load * 0.01
        return baseline_input_power


class WH2_test_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input power (kW)'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        annual_energy_savings = buildings('WH2_test_annual_energy_savings', period)
        baseline_input_power = buildings('WH2_test_baseline_input_power', period)

        input_power = (100 - annual_energy_savings) * (baseline_input_power / 100)
        return input_power


class WH2_test_peak_demand_savings_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand savings capacity'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        baseline_input_power = buildings('WH2_test_baseline_input_power', period)
        baseline_peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['baseline_peak_adjustment']['WH2_test']
        input_power = buildings('WH2_test_input_power', period)
        peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['peak_adjustment']['WH2_test']
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor['firmness_factor']['WH2_test']

        peak_demand_savings_capacity = (baseline_input_power * baseline_peak_adjustment_factor) - (input_power * peak_adjustment_factor * firmness_factor)
        return peak_demand_savings_capacity
    

class WH2_test_peak_demand_annual_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand annual savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #baseline input power
        com_peak_load = buildings('WH2_test_com_peak_load', period)
        baseline_input_power = com_peak_load * 0.01

        #baseline peak adjustment factor
        baseline_peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['baseline_peak_adjustment']['WH2_test']

        #input power
        annual_energy_savings = buildings('WH2_test_annual_energy_savings', period)
        input_power = (100 - annual_energy_savings) * (baseline_input_power / 100)

        #peak adjustment factor
        peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['peak_adjustment']['WH2_test']

        #firmness factor
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor['firmness_factor']['WH2_test']

        #peak demand savings capacity
        summer_peak_demand_reduction_duration = 6
        peak_demand_annual_savings = ((baseline_input_power * baseline_peak_adjustment_factor) - (input_power * peak_adjustment_factor * firmness_factor)) * summer_peak_demand_reduction_duration
        
        return peak_demand_annual_savings
        

class WH2_test_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand reduction capacity (kW)'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        peak_demand_savings_capacity = buildings('WH2_test_peak_demand_savings_capacity', period)
        summer_peak_reduction = parameters(period).PDRS.PDRS_wide_constants['daily_peak_window_hours']
        lifetime = parameters(period).ESS.HEAB.table_F16_1['lifetime']

        peak_demand_reduction_capacity = peak_demand_savings_capacity * summer_peak_reduction * lifetime
        return peak_demand_reduction_capacity


class WH2_test_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'label' : 'The number of PRCs for WH2_test',
        'variable-type' : 'output'
    }

    def formula(buildings, period, parameters):
        peak_demand_capacity = buildings('WH2_test_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('WH2_test_get_network_loss_factor_by_postcode', period)
        kw_to_0_1kw = 10
        replacement_activity = buildings('WH2_test_replacement_activity', period)

        WH2_test_eligible_PRCs = np.select(
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
                WH2_test_eligible_PRCs <= 0, WH2_test_eligible_PRCs > 0
            ],
            [
                0, WH2_test_eligible_PRCs
            ])
        return result_to_return