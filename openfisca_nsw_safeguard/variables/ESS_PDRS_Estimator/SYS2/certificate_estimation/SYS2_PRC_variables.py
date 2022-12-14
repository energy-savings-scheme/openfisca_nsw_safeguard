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
        'display_question' : 'What type of pool pump is installed?',
        'sorting' : 5
    }

class SYS2InputPowerEligibility(Enum):
    pump_under_100w = 'Less than 100 watts'
    pump_100w_to_599w = '101 watts to 599 watts'
    pump_600w_to_1700w = '600 watts to 1700 watts'
    pump_1701w_to_2500w = '1701 watts to 2500 watts'
    pump_2501w_to_3450w = '2501 watts to 3450 watts'
    pump_more_than_3451w = 'More than 3450 watts'


class SYS2_input_power_eligibility(Variable):
    value_type = Enum
    entity = Building
    definition_period = ETERNITY
    possible_values = SYS2InputPowerEligibility
    default_value = SYS2InputPowerEligibility.pump_600w_to_1700w
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Pool pump input power (watts)',
        'display_question' : 'What is the input power of the replacement pool pump?',
        'sorting' : 7
    }

class SYS2_input_power_ESCS_eligibility_int(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      input_power_eligibility = buildings('SYS2_input_power_eligibility', period)
      pool_pump_type_single = buildings('SYS2_pool_pump_type', period)

      input_power_ESC_eligibility_int = np.select([
            (input_power_eligibility == SYS2InputPowerEligibility.pump_under_100w),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_100w_to_599w),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_600w_to_1700w),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_1701w_to_2500w) * (pool_pump_type_single == SYS2PoolPumpType.single_speed_pool_pump),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_1701w_to_2500w) * (pool_pump_type_single != SYS2PoolPumpType.single_speed_pool_pump),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_2501w_to_3450w) * (pool_pump_type_single == SYS2PoolPumpType.single_speed_pool_pump),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_2501w_to_3450w) * (pool_pump_type_single != SYS2PoolPumpType.single_speed_pool_pump),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_more_than_3451w),
        ],
        [
             False,
             False,
             True,
             False,
             True,
             False,
             True,
             False
        ])
      return input_power_ESC_eligibility_int


class SYS2_input_power_PRCS_eligibility_int(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      input_power_eligibility = buildings('SYS2_input_power_eligibility', period)
      pool_pump_type_single = buildings('SYS2_pool_pump_type', period)
      input_power_PRC_eligibility_int = np.select([
            (input_power_eligibility == SYS2InputPowerEligibility.pump_under_100w),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_100w_to_599w),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_600w_to_1700w),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_1701w_to_2500w) * (pool_pump_type_single == SYS2PoolPumpType.single_speed_pool_pump),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_1701w_to_2500w) * (pool_pump_type_single != SYS2PoolPumpType.single_speed_pool_pump),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_2501w_to_3450w) * (pool_pump_type_single == SYS2PoolPumpType.single_speed_pool_pump),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_2501w_to_3450w) * (pool_pump_type_single != SYS2PoolPumpType.single_speed_pool_pump),
            (input_power_eligibility == SYS2InputPowerEligibility.pump_more_than_3451w),
        ],
        [
             False,
             False,
             True,
             False,
             True,
             False,
             True,
             False
        ])
      return input_power_PRC_eligibility_int


class SYS2_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      pool_size = buildings('SYS2_pool_size_int', period)
      pool_pump_type = buildings('SYS2_pool_pump_type', period)
      star_rating = buildings('SYS2_star_rating', period)

      input_power = parameters(period).PDRS.pool_pumps.table_sys2_2['input_power'][pool_size][star_rating][pool_pump_type]
      return input_power


class SYS2_DNSP_Options(Enum):
    Ausgrid = 'Ausgrid'
    Endeavour = 'Endeavour'
    Essential = 'Essential'


class SYS2_DNSP(Variable):
     # this variable is used as the second input on all estimator certificate calculation pages
    value_type = Enum
    entity = Building
    possible_values = SYS2_DNSP_Options
    default_value = SYS2_DNSP_Options.Ausgrid
    definition_period = ETERNITY
    label = "Distribution Network Service Provider"
    metadata = {
        'variable-type': 'user-input',
        'display_question': 'Who is your Distribution Network Service Provider?',
        'sorting' : 2,
        'label': "Distribution Network Service Provider"
    }


class SYS2_network_loss_factor(Variable):
    reference = 'table_A3_network_loss_factors'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    
    def formula(buildings, period, parameters):
        distribution_district = buildings('SYS2_DNSP', period)
        network_loss_factor = parameters(period).PDRS.table_A3_network_loss_factors['network_loss_factor'][distribution_district]
        return network_loss_factor