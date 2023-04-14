import enum
from multiprocessing import pool
import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class SYS2PoolSize(Enum):
    pool_under_20000_L = 'Less than 20,000 litres'
    pool_20000_to_30000_L = '20,000 to 30,000 litres'
    pool_30001_to_40000_L = '30,001 to 40,000 litres'
    pool_40001_to_50000_L = '40,001 to 50,000 litres'
    pool_50001_to_60000_L = '50,001 to 60,000 litres'
    pool_60001_to_70000_L = '60,001 to 70,000 litres'
    over_70001_L = 'More than 70,000 litres'


class SYS2_pool_size(Variable):
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


class SYS2_pool_size_int(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      pool_size = buildings('SYS2_pool_size', period)
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
      return pool_size_int


class SYS2_baseline_input_power(Variable):
      value_type = float
      entity = Building
      definition_period = ETERNITY

      def formula(buildings, period, parameters):
        pool_size = buildings('SYS2_pool_size_int', period)

        baseline_input_power = parameters(period).PDRS.pool_pumps.table_sys2_1['baseline_input_power'][pool_size]
        return baseline_input_power


class SYS2PoolPumpType(Enum):
    single_speed_pool_pump = 'Single speed'
    fixed_speed_pool_pump = 'Two speed'
    variable_speed_pool_pump = 'Variable speed'
    multiple_speed_pool_pump = 'Multi speed'


# class SYS2_pool_pump_type_string(Variable):
#     value_type = str
#     entity = Building
#     definition_period = ETERNITY

#     def formula(buildings, period, parameters):
#       product_class = buildings('SYS2_pool_pump_type', period)
      
#       product_class = np.select([
#         product_class == 'single speed',
#         product_class == 'two speed',
#         product_class == 'variable speed',
#         product_class == 'multi speed'
#       ], 
#       [
#         SYS2PoolPumpType.single_speed_pool_pump,
#         SYS2PoolPumpType.fixed_speed_pool_pump,
#         SYS2PoolPumpType.variable_speed_pool_pump,
#         SYS2PoolPumpType.multiple_speed_pool_pump
#       ])
      
#       return product_class


class SYS2_pool_pump_type(Variable):
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


class SYS2_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      pool_size = buildings('SYS2_pool_size_int', period)
      pool_pump_type = buildings('SYS2_pool_pump_type', period)
      star_rating = buildings('SYS2StarRatingString', period)

      input_power = parameters(period).PDRS.pool_pumps.table_sys2_2['input_power'][pool_size][star_rating][pool_pump_type]
      return input_power


class SYS2_get_network_loss_factor_by_postcode(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'input',
        'sorting' : 2,
        'label' : 'Network loss factor is calculated automatically from your postcode. If you have a 0 here, please check your postcode is correct. If the postcode has more than one distribution network service provider, we have chosen the network factor loss with the lowest value.'
    }
    def formula(building, period, parameters):
        postcode = building('SYS2_PDRS__postcode', period)
        network_loss_factor = parameters(period).PDRS.table_network_loss_factor_by_postcode

        return network_loss_factor.calc(postcode)