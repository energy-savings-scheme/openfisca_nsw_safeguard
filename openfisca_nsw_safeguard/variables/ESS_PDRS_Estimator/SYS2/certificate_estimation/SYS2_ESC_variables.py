import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for SYS2 ESC Calculation
    These variables use Rule tables
"""
class SYS2_PDRS__postcode(Variable):
    # using to get the regional network factor
    # this variable is used as the first input on all estimator certificate calculation pages
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'alias' : 'PDRS Postcode',
        'label': 'Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1
        }


class SYS2_replacement_activity(Variable):
    value_type = bool
    default_value = True
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'user-input',
        'label': 'Replacement or new installation activity',
        'display_question': 'Is the activity a replacement of existing equipment?',
        'sorting' : 3
    }

class SYS2InputPowerEligibility(Enum):
    pump_under_100w = 'Less than 100 watts'
    pump_101w_to_599w = '101 watts to 599 watts'
    pump_600w_to_1700w = '600 watts to 1700 watts'
    pump_1701w_2500w = '1701 watts to 2500 watts'
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


class SYS2_input_power_eligibility_int(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      pool_size = buildings('SYS2_pool_size', period)
      pool_size_int = np.select([
          (pool_size == SYS2InputPowerEligibility.pool_under_20000_L),
          (pool_size == SYS2InputPowerEligibility.pool_20000_to_30000_L),
          (pool_size == SYS2InputPowerEligibility.pool_30001_to_40000_L ),
          (pool_size == SYS2InputPowerEligibility.pool_40001_to_50000_L ),
          (pool_size == SYS2InputPowerEligibility.pool_50001_to_60000_L ),
          (pool_size == SYS2InputPowerEligibility.pool_60001_to_70000_L ),
          (pool_size == SYS2InputPowerEligibility.over_70001_L)
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