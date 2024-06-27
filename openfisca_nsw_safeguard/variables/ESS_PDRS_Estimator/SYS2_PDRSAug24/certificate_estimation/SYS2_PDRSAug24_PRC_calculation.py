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
        baseline_peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['baseline_peak_adjustment']['SYS2']
        input_power = buildings('SYS2_PDRSAug24_input_power', period)
        peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['peak_adjustment']['SYS2']
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor['firmness_factor']['SYS2']

        peak_demand_savings_capacity = ((baseline_input_power * baseline_peak_adjustment_factor) - (input_power * peak_adjustment_factor)) * firmness_factor

        return peak_demand_savings_capacity
    

class SYS2PoolSize(Enum):
    pool_under_20000_L = 'Less than 20,000 litres'
    pool_20000_to_30000_L = '20,000 to 30,000 litres'
    pool_30001_to_40000_L = '30,001 to 40,000 litres'
    pool_40001_to_50000_L = '40,001 to 50,000 litres'
    pool_50001_to_60000_L = '50,001 to 60,000 litres'
    pool_60001_to_70000_L = '60,001 to 70,000 litres'
    over_70001_L = 'More than 70,000 litres'


class SYS2_PDRSAug24_pool_size_savings(Variable):
    value_type = Enum
    entity = Building
    definition_period = ETERNITY
    possible_values = SYS2PoolSize
    default_value = SYS2PoolSize.pool_30001_to_40000_L
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Pool size (litres)',
        'display_question' : 'What is the volume of the pool?',
        'sorting' : 3
    }

    
class SYS2PoolPumpType(Enum):
    single_speed_pool_pump = 'Single speed'
    fixed_speed_pool_pump = 'Two speed'
    variable_speed_pool_pump = 'Variable speed'
    multiple_speed_pool_pump = 'Multi speed'


class SYS2_PDRSAug24_pool_pump_type_savings(Variable):
    value_type = Enum
    entity = Building
    default_value = SYS2PoolPumpType.variable_speed_pool_pump
    possible_values = SYS2PoolPumpType
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Pool pump type',
        'display_question' : 'What is the pool pump type?',
        'sorting' : 5
    }


class SYS2StarRating(Enum):
    #New End-User Equipment must achieve a minimum 4.5 star rating to be eligible
    four_and_a_half_stars = '4.5'
    five_stars = '5'
    five_and_a_half_stars = '5.5'
    six_stars = '6'
    seven_stars = '7'
    eight_stars = '8'
    nine_stars = '9'
    ten_stars = '10'

    
class SYS2_PDRSAug24_star_rating_peak_savings(Variable):
    value_type = Enum
    entity = Building
    default_value = SYS2StarRating.four_and_a_half_stars
    possible_values = SYS2StarRating
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'New equipment star rating',
        'display_question' : 'What is the star rating of your new equipment? (Equipment must achieve a 4.5 star rating or higher)',
        'sorting' : 5
    }


class SYS2_PDRSAug24_peak_demand_annual_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand annual savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #pool size
        pool_size = buildings('SYS2_PDRSAug24_pool_size', period)
        pool_size_int = np.select([
            (pool_size == SYS2PoolSize.pool_under_20000_L),
            (pool_size == SYS2PoolSize.pool_20000_to_30000_L),
            (pool_size == SYS2PoolSize.pool_30001_to_40000_L ),
            (pool_size == SYS2PoolSize.pool_40001_to_50000_L ),
            (pool_size == SYS2PoolSize.pool_50001_to_60000_L ),
            (pool_size == SYS2PoolSize.pool_60001_to_70000_L ),
            (pool_size == SYS2PoolSize.over_70001_L)
        ],
        [
            'under_20000_L',
            '20000_to_30000_L',
            '30001_to_40000_L',
            '40001_to_50000_L',
            '50001_to_60000_L',
            '60001_to_70000_L',
            'over_70000_L'
        ])

        #baseline input power
        baseline_input_power = parameters(period).PDRS.pool_pumps.table_SYS2_PDRSAug24_1['baseline_input_power'][pool_size_int]
        
        #baseline peak adjustment factor
        baseline_peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['baseline_peak_adjustment']['SYS2']

        #input power
        pool_pump_type = buildings('SYS2_PDRSAug24_pool_pump_type', period)
        star_rating = buildings('SYS2_PDRSAug24_star_rating', period)
        
        input_power = parameters(period).PDRS.pool_pumps.table_SYS2_PDRSAug24_2['input_power'][pool_size_int][star_rating][pool_pump_type]
     
        #peak adjustment factor
        peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['peak_adjustment']['SYS2']

        #firmness factor
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor['firmness_factor']['SYS2']

        #peak demand savings capacity
        peak_demand_savings_capacity = ((baseline_input_power * baseline_peak_adjustment_factor) - (input_power * peak_adjustment_factor)) * firmness_factor

        #peak demand annual savings 
        summer_peak_demand_reduction_duration = 6   
        lifetime = 12

        peak_demand_annual_savings = peak_demand_savings_capacity * summer_peak_demand_reduction_duration *lifetime
        
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
        lifetime = 12

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
        replacement_activity = buildings('SYS2_PDRSAug24_replacement_activity', period)

        SYS2_PDRSAug24_eligible_PRCs = np.select(
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
                SYS2_PDRSAug24_eligible_PRCs <= 0, SYS2_PDRSAug24_eligible_PRCs > 0
            ],
            [
                0, SYS2_PDRSAug24_eligible_PRCs
            ])
        return result_to_return