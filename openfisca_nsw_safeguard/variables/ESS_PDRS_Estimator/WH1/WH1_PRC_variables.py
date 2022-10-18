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

class WH1_gas_annual_energy_savings(Variable):
    # Annual Gas Energy used by the End-User equipment
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        # HPgas from VEU registry
        'display_question': 'Annual gas energy savings (Gj/year)'
    }


""" These variables use Rule tables
"""
class network_loss_factor_options(Enum):
    Ausgrid = 1.04
    Endeavour = 1.05
    Essential = 1.05


class PDRS_network_loss_factor(Variable):
    #pulls in to PRC calculations
    value_type = float
    entity = Building
    definition_period = ETERNITY
    
    def formula(building, period):
        network_loss = building('WH1_Provider_to_network_loss_factor_enum', period)
        return np.select(
            [
                network_loss == network_loss_factor_options.Ausgrid,
                network_loss == network_loss_factor_options.Endeavour,
                network_loss == network_loss_factor_options.Essential     
            ],
            [  
                1.04,
                1.05,
                1.05
            ])


class WH1_Provider_to_network_loss_factor_enum(Variable):
    value_type = Enum
    entity = Building
    possible_values = network_loss_factor_options
    default_value = network_loss_factor_options.Ausgrid
    definition_period = ETERNITY
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Distribution District",
        "display_question": "Who is your network service provider?"
    }
 