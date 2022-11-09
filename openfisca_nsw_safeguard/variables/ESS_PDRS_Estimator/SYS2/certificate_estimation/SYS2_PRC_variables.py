import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class SYS2PoolSize(Enum):
    pool_under_20000 = 'Less than 20,000 litres'
    pool_20000_to_30000 = '20,000 to 30,000 litres'
    pool_30001_to_40000 = '30,001 to 40,000 litres'
    pool_40001_to_50000 = '40,001 to 50,000 litres'
    pool_50001_to_60000 = '50,001 to 60,000 litres'
    pool_60001_to_70000 = '60,001 to 70,000 litres'
    pool_over_70001_L = 'More than 70,000 litres'


class SYS2_pool_size(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS2PoolSize
    default_value = SYS2PoolSize.pool_20000_to_30000
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Pool size (litres)',
        'display_question' : 'What is the volume of the pool?',
        'sorting' : 3
    }


class SYS2_baseline_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      pool_size = buildings('SYS2_pool_size', period)
      baseline_input = parameters(period).PDRS.pool_pumps.table_sys2_1['baseline_input_power'][pool_size]
    
      return baseline_input


class SYS2PoolPumpType(Enum):
    single_speed_pool_pump = 'Single speed pool pump',
    fixed_speed_pool_pump = 'Fixed speed pool pump'
    variable_speed_pool_pump = 'Variable speed pool pump'
    multiple_speed_pool_pump = 'Multiple speed pool pump'


class SYS2_pool_pump_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS2PoolPumpType
    default_value = SYS2PoolPumpType.variable_speed_pool_pump
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Pool pump type',
        'display_question' : 'What type of pool pump have you installed',
        'sorting' : 5
    }


class SYS2_pool_pump_int(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      pool_pump_type = buildings('SYS2_pool_size', period)
      pool_pump_type_int = np.select([
        pool_pump_type == SYS2PoolPumpType.single_speed_pool_pump,
        pool_pump_type == SYS2PoolPumpType.fixed_speed_pool_pump,
        pool_pump_type == SYS2PoolPumpType.variable_speed_pool_pump,
        pool_pump_type == SYS2PoolPumpType.multiple_speed_pool_pump
      ],
      [
        'single_speed_pool_pump',
        'fixed_speed_pool_pump',
        'variable_speed_pool_pump',
        'multiple_speed_pool_pump'
      ])
      
      return pool_pump_type_int

##still need to do star rating

class SYS2_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      pool_size = buildings('SYS2_pool_size', period)
      pool_pump_type = buildings('SYS2_pool_pump_type', period)
      star_rating = buildings('SYS2_star_rating', period)
      input_power = parameters(period).PDRS.pool_pumps.table_sys2_2['input_power'][pool_size][pool_pump_type]
    

      input_power = pool_size
      return input_power
