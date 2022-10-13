import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for WH1 PRC Calculation
"""

""" Values shared with ESC variables WH1_ESC_variables 
    WH1_com_peak_load
"""
class WH1_annual_energy_savings(Variable):
    #Annual Gas Energy used by the End-User equipment
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY