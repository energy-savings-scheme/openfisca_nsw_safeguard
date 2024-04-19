from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


""" Parameters for F17 ESC Calculation
"""


class F17_ESS__postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata={
        'variable-type' : 'user-input',
        'alias' : 'ESS Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1,
        'label': 'Postcode'
    }


class F17_installation_activity(Variable):
    value_type = bool
    default_value = True
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'user-input',
        'label': 'New installation activity',
        'display_question': 'Is the activity a new installation?',
        'sorting' : 2
    }


class F17_com_peak_load(Variable):
    reference = 'MJ per day'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'ComPkLoad (MJ/day)'
    metadata = {
        'display_question': 'Peak daily (winter) load based on the address of the site where the End-User Equipment is installed',
        'sorting' : 3,
        'label': 'ComPkLoad (MJ/day)',
        'variable-type': 'input'
    }


class F17_HP_gas(Variable):
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HPGas (GJ/year)'
    metadata = {
        'display_question': 'Annual gas energy used by the End-User Equipment',
        'sorting' : 4,
        'label': 'HPGas (GJ/year)',
        'variable-type': 'input'
    }


class F17_HP_elec(Variable):
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HPElec (GJ/year)'
    metadata = {
        'display_question': 'Annual electrical energy used by the End-User Equipment',
        'sorting' : 5,
        'label': 'HPElec (GJ/year)',
        'variable-type': 'input'
    }


class F17_regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor from ESS Table A24'
    
    def formula(buildings, period, parameters):
        postcode = buildings('F17_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)