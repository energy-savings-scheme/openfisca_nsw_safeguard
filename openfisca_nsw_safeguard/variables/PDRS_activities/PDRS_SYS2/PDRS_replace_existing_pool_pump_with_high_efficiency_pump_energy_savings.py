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
        input_power = buildings('PDRS_replace_existing_pool_pump_with_high_efficiency_pump_input_power', period)
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
            'pool_under_20000_L',
            'pool_20000_to_30000_L',
            'pool_30001_to_40000_L',
            'pool_40001_to_50000_L',
            'pool_50001_to_60000_L',
            'pool_60001_to_70000_L',
            'pool_over_70000_L',
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
                                        (new_pump_pool_volume <= 40000)
                                    ),
                                    (
                                        (new_pump_pool_volume >= 40001) * 
                                        (new_pump_pool_volume <= 50000)
                                    ),
                                    (
                                        (new_pump_pool_volume >= 50001) * 
                                        (new_pump_pool_volume <= 60000)
                                    ),
                                    (
                                        (new_pump_pool_volume >= 60001) * 
                                        (new_pump_pool_volume <= 70000)
                                    ),
                                    (new_pump_pool_volume >= 70001),
        ],
        [
            'pool_under_20000_L',
            'pool_20000_to_30000_L',
            'pool_30001_to_40000_L',
            'pool_40001_to_50000_L',
            'pool_50001_to_60000_L',
            'pool_60001_to_70000_L',
            'pool_over_70000_L',
        ])
        star_rating = buildings('ESS_and_PDRS_new_pump_star_rating', period)
        pump_type = buildings('ESS_and_PDRS_new_pool_pump_type', period)
        input_power = (parameters(period).
            PDRS.pool_pumps.table_sys2_2.input_power
            [pool_volume][star_rating][pump_type])
        return input_power

class PDRS_new_pump_pool_volume(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the volume of the pool the new pool pump is being installed in?'
    metadata = {
        'alias':  'Pool volume.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }

class ESS_PDRS_NewPumpStarRating(Enum):
    zero_stars = u'Pump has a star rating of 0 stars.'
    one_star = u'Pump has a star rating of 1 star.'
    one_and_a_half_star = u'Pump has a star rating of 1.5 star.'
    two_stars = u'Pump has a star rating of 2 stars.'
    two_and_a_half_stars = u'Pump has a star rating of 2.5 stars.'
    three_stars = u'Pump has a star rating of 3 stars.'
    three_and_a_half_stars = u'Pump has a star rating of 3.5 stars.'
    four_stars = u'Pump has a star rating of 4 stars.'
    four_and_a_half_stars = u'Pump has a star rating of 4.5 stars.'
    five_stars = u'Pump has a star rating of 5 stars.'
    five_and_a_half_stars = u'Pump has a star rating of 5.5 stars.'
    six_stars = u'Pump has a star rating of 6 stars.'
    six_and_a_half_stars = u'Pump has a star rating of 6.5 stars.'
    seven_stars = u'Pump has a star rating of 7 stars.'
    seven_and_a_half_stars = u'Pump has a star rating of 7.5 stars.'
    eight_stars = u'Pump has a star rating of 8 stars.'
    eight_and_a_half_stars = u'Pump has a star rating of 8.5 stars.'
    nine_stars = u'Pump has a star rating of 9 stars.'
    nine_and_a_half_stars = u'Pump has a star rating of 9.5 stars.'    
    ten_stars = u'Pump has a star rating of 10 stars.'


class ESS_and_PDRS_new_pump_star_rating(Variable):
    value_type = Enum
    possible_values = ESS_PDRS_NewPumpStarRating
    default_value = ESS_PDRS_NewPumpStarRating.zero_stars
    entity = Building
    definition_period = ETERNITY
    label = 'What is the star rating of the new pool pump?'
    metadata = {
        'alias':  'New pump star rating.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }


class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_meets_all_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the relevant Eligibility, Equipment and Implementation Requirements?'
    metadata = {
        'alias':  'PDRS Pool Pump Meets All Requirements.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }

    def formula(buildings, period, parameters):
        meets_eligibility_requirements = buildings(
            'PDRS_replace_existing_pool_pump_with_high_efficiency_pump_meets_eligibility_requirements', period)
        meets_equipment_requirements = buildings(
            'PDRS_replace_existing_pool_pump_with_high_efficiency_pump_meets_equipment_requirements', period)        
        meets_implementation_requirements = buildings(
            'PDRS_replace_existing_pool_pump_with_high_efficiency_pump_meets_implementation_requirements', period)
        return(
            meets_eligibility_requirements *
            meets_equipment_requirements * 
            meets_implementation_requirements
        )
