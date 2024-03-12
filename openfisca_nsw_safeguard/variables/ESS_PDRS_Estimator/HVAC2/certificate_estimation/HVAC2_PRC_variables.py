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
"""

""" These variables use GEMS Registry data
"""
class HVAC2_input_power(Variable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Rated cooling input power (kW)'
    metadata = {
        'display_question' : 'Rated cooling input power at 35C as recorded in the GEMS registry',
        'label' : 'Rated cooling input power (kW)',
        'variable-type': 'user-input',
        'sorting' : 12
    }


class HVAC2_get_network_loss_factor_by_postcode(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'input',
        'sorting' : 2,
        'label' : 'Network loss factor is calculated automatically from your postcode. If you have a 0 here, please check your postcode is correct. If the postcode has more than one distribution network service provider, we have chosen the network factor loss with the lowest value.'
    }
    def formula(building, period, parameters):
        postcode = building('HVAC2_PDRS__postcode', period)
        network_loss_factor = parameters(period).PDRS.table_network_loss_factor_by_postcode

        return network_loss_factor.calc(postcode)