from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


""" Parameters for RF2 ESC Calculation
    These variables use GEMS Registry data
"""
class RF2_total_energy_consumption(Variable):
  #Total energy consumption
  reference = 'kWh per day'
  value_type = float
  entity = Building
  definition_period = ETERNITY
  label = 'TEC (kWh/day)'
  metadata = {
    'display_question' : 'Total Energy Consumption'
    'sorting' : 
  }


class RF2_af(Variable):
  value_type = float
  entity = Building
  definition_period = ETERNITY


class RF2_baseline_EEI(Variable):
  value_type = float
  entity = Building
  definition_period = ETERNITY


class RF2_product_EEI(Variable):
  value_type = float
  entity = Building
  definition_period = ETERNITY