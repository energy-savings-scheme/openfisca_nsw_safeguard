from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building

import numpy as np


""" Parameters for BESS2 PRC Calculation
    These variables use Rule tables and CEC Approved Battery Registry data
"""


class BESS2_V5Nov24_PDRS__postcode(BaseVariable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'user-input',
        'label': 'Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1        
    }


class BESS2_V5Nov24_installation_activity(BaseVariable):
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


class BESS2_V5Nov24_usable_battery_capacity(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'output',
        'label': 'Usable battery capacity (kWh)'
    }

    def formula(buildings, period, parameters):
        # Get nominal battery capacity
        nominal_battery_capacity = buildings('BESS2_V5Nov24_nominal_battery_capacity', period)

        # Apply 90% rule
        adjusted_capacity = nominal_battery_capacity * 0.9

        # Cap at 28 kWh
        cap = 28.0

        # Take the lower of the two
        capped_capacity = np.minimum(adjusted_capacity, cap)

        # Final rule: if nominal >= 50 → return 0
        usable_battery_capacity = np.where(
            nominal_battery_capacity >= 50,
            0,
            capped_capacity
        )

        return usable_battery_capacity


class BESS2_V5Nov24_nominal_battery_capacity(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'user-input',
        'label': 'Nominal battery capacity (kWh)',
        'display_question': 'What is the nominal battery capacity (kWh)?',
        'sorting': 3
    }


class BESS2_V5Nov24_get_network_loss_factor_by_postcode(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'input',
        'label' : 'Network loss factor is calculated automatically from your postcode. If you have a 0 here, please check your postcode is correct. If the postcode has more than one distribution network service provider, we have chosen the network factor loss with the lowest value.'
    }
    def formula(building, period, parameters):
        postcode = building('BESS2_V5Nov24_PDRS__postcode', period)
        network_loss_factor = parameters(period).PDRS.table_network_loss_factor_by_postcode

        return network_loss_factor.calc(postcode)
