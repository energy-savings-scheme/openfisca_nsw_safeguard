from decimal import FloatOperation
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

""" These variables use VEU Registry data
"""
class WH1_annual_energy_savings(Variable):
    #Annual Gas Energy used by the End-User equipment
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY


""" These variables use Rule tables
"""
class network_loss_factor(Enum):
    Ausgrid = 1.04
    Endeavour = 1.05
    Essential = 1.05


class PDRS_network_loss_factor(Variable):
    #pulls in to PRC calculations
    value_type = float
    entity = Building
    definition_period = ETERNITY


class network_loss_factor_enum(Variable):
    value_type = Enum
    entity = Building
    possible_values = network_loss_factor
    default_value = network_loss_factor.Ausgrid
    definition_period = ETERNITY
 
    def formula(building, period):
        network_loss = building('PDRS_network_loss_factor', period)
        return np.select(
                [
                    network_loss.Ausgrid,
                    network_loss.Endeavour,
                    network_loss.Essential     
                ],
                [  
                    network_loss_factor == 1.04,
                    network_loss_factor == 1.05,
                    network_loss_factor == 1.05
                ])