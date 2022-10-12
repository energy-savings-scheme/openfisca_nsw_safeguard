import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for WH1 ESC Calculation
    These variables use VEU Registry data
"""
class WH1_HP_capacity_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY


class WH1_WH_capacity_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY


class WH1_HP_gas(Variable):
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY


""" These variables use Rule tables
"""

