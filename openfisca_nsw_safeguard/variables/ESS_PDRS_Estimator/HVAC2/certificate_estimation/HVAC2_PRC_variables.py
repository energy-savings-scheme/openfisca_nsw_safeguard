from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


""" Parameters for HVAC2 PRC Calculation
"""

""" Values shared with ESC variables HVAC2_ESC_variables 
    HVAC2_cooling_capacity_input
    HVAC2_baseline_AEER_input
    HVAC2_lifetime_value
"""

""" These variables use GEMS Registry data
"""
class HVAC2_input_power(Variable):
    reference = 'unit in '
    value_type = float
    entity = Building
    definition_period = ETERNITY

    
class HVAC2_Energy_Provider_Options(Enum):
    Ausgrid = 'Ausgrid'
    Endeavour = 'Endeavour'
    Essential = 'Essential'


class HVAC2_Energy_Provider(Variable):
    value_type = Enum
    entity = Building
    possible_values = HVAC2_Energy_Provider_Options
    default_value = HVAC2_Energy_Provider_Options.Ausgrid
    definition_period = ETERNITY
    label = 'Energy provider'
    metadata={
        "variable-type": "user-input",
        "alias":"Energy provider",
        "display_question": "Please select your energy provider."
        }


class HVAC2_network_loss_factor(Variable):
    reference = 'table_A3_network_loss_factors'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    
    def formula(buildings, period, parameters):
        network_provider = buildings('HVAC2_Energy_Provider', period)
        network_loss_factor = parameters(period).PDRS.table_A3_network_loss_factors[network_provider]
        return network_loss_factor
