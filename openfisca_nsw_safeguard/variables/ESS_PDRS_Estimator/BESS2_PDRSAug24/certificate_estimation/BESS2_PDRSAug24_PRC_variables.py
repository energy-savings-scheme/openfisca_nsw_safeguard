from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


""" Parameters for BESS2 PRC Calculation
    These variables use Rule tables and CEC Approved Battery Registry data
"""


class BESS2_PDRSAug24_PDRS__postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'user-input',
        'label': 'Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1        
    }


class BESS2_PDRSAug24_installation_activity(Variable):
    value_type = bool
    default_value = True
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'user-input',
        'label': 'New installation or replacement activity',
        'display_question': 'Is the activity a new installation?',
        'sorting' : 2
    }


class BESS2_PDRSAug24_usable_battery_capacity(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata={
        'variable-type' : 'user-input',
        'label': 'Usable battery capacity',
        'display_question' : 'What is the battery capacity?',
        'sorting' : 3        
    }


class BESS2_PDRSAug24_get_network_loss_factor_by_postcode(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'input',
        'label' : 'Network loss factor is calculated automatically from your postcode. If you have a 0 here, please check your postcode is correct. If the postcode has more than one distribution network service provider, we have chosen the network factor loss with the lowest value.'
    }
    def formula(building, period, parameters):
        postcode = building('BESS2_PDRSAug24_PDRS__postcode', period)
        network_loss_factor = parameters(period).PDRS.table_network_loss_factor_by_postcode

        return network_loss_factor.calc(postcode)