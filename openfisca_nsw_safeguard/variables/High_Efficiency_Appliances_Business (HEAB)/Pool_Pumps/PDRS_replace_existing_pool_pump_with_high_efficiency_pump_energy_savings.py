from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021

import numpy as np

class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_peak_demand_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the peak demand savings created by replacing a pool pump?'
    metadata = {
        'alias':  'Replace pump peak demand savings.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }

    def formula(buildings, period, parameters):
        baseline_input_power = buildings('PDRS_replace_existing_pool_pump_with_high_efficiency_pump_baseline_input_power', period)
        baseline_peak_adjustment_factor = (
                                    parameters(period).
                                    PDRS.table_A27_end_use_equipment_factors
                                    ['pool_pumps']['baseline_peak_load_adjustment_factor']
                                            )
        input_power = buildings('PDRS_new_pump_input_power', period)
        peak_load_adjustment_factor = (
                                    parameters(period).
                                    PDRS.table_A27_end_use_equipment_factors
                                    ['pool_pumps']['baseline_peak_load_adjustment_factor']
                                            )
        firmness_factor = (
                                    parameters(period).
                                    PDRS.table_A27_end_use_equipment_factors
                                    ['pool_pumps']['firmness_factor']
        )
        peak_demand_reduction_savings = (
                                (
                                    baseline_input_power *
                                    baseline_peak_adjustment_factor - 
                                    input_power *
                                    peak_load_adjustment_factor
                                ) *
                                firmness_factor
                            )    
        return peak_demand_reduction_savings


class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_baseline_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the baseline power input for the Replace Pool Pump activity?'
    metadata = {
        'alias':  'Replace pump baseline input power.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }

    def formula(buildings, period, parameters):
        new_pump_pool_volume = buildings('PDRS_new_pump_pool_volume', period)
        pool_volume = np.select([
                                    (new_pump_pool_volume < 20000),
                                    (
                                        (new_pump_pool_volume >= 20000) * 
                                        (new_pump_pool_volume <= 30000)
                                    ),
                                    (
                                        (new_pump_pool_volume >= 30001) * 
                                        (new_pump_pool_volume < 40000)
                                    ),
                                    (
                                        (new_pump_pool_volume >= 40001) * 
                                        (new_pump_pool_volume < 50000)
                                    ),
                                    (
                                        (new_pump_pool_volume >= 50001) * 
                                        (new_pump_pool_volume < 60000)
                                    ),
                                    (
                                        (new_pump_pool_volume >= 60001) * 
                                        (new_pump_pool_volume < 70000)
                                    ),
                                    (new_pump_pool_volume >= 70001),
        ],
        [
            'under_20000_L',
            '20000_to_30000_L',
            '30001_to_40000_L',
            '40001_to_50000_L',
            '50001_to_60000_L',
            '60001_to_70000_L',
            'over_70000_L',
        ])
        baseline_input_power = (
            parameters(period).PDRS.pool_pumps.table_sys2_1.baseline_input_power[pool_volume])
        return baseline_input_power


class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the power input for the Replace Pool Pump activity?'
    metadata = {
        'alias':  'Replace pump baseline input power.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }


class PDRS_new_pump_pool_volume(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the volume of the pool the new pool pump is being installed in?'
    metadata = {
        'alias':  'Pool volume.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }



class PDRS_new_pump_star_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the star rating of the new pool pump?'
    metadata = {
        'alias':  'New pump star rating.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }

class PDRS_new_pump_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the input power of the new pool pump?'
    metadata = {
        'alias':  'New pump star input power.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }
