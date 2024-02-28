import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for WH2_test ESC Calculation
    These variables use VEU Registry data
"""
class WH2_test_HP_capacity_factor(Variable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HPCap (kW)'
    metadata = {
        'display_question': 'Total rated capacity of the heat pump water heater(s) being installed',
        'sorting' : 5,
        'variable-type': 'input',
        'label': 'HPCap (kW)'
    }


class WH2_test_WH_capacity_factor(Variable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'WHCap (kW)'
    metadata = {
        'display_question': 'Total rated capacity (kW) of the End-User Equipment being replaced',
        'sorting' : 6,
        'variable-type': 'input',
        'label': 'WHCap (kW)'
    }


class WH2_test_HP_gas(Variable):
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HPGas (GJ/year)'
    metadata = {
        'display_question': 'Annual gas energy used by the End-User Equipment',
        'sorting' : 7,
        'label': 'HPGas (GJ/year)',
        'variable-type': 'input'
    }


class WH2_test_com_peak_load(Variable):
    reference = 'MJ per day'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'ComPkLoad (MJ/day)'
    metadata = {
        'display_question': 'Peak daily (winter) load based on the address of the site where the End-User Equipment is installed',
        'sorting' : 9,
        'label': 'ComPkLoad (MJ/day)',
        'variable-type': 'input'
    }


class WH2_test_HP_elec(Variable):
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HPElec (GJ/year)'
    metadata = {
        'display_question': 'Annual electrical energy used by the End-User Equipment',
        'sorting' : 8,
        'label': 'HPElec (GJ/year)',
        'variable-type': 'input'
    }


class WH2_test_regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor from ESS Table A24'
    
    def formula(buildings, period, parameters):
        postcode = buildings('WH2_test_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)


class WH2_test_replacement_activity(Variable):
    value_type = bool
    default_value = True
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'user-input',
        'label': 'Replacement or new installation activity',
        'display_question': 'Is the activity the replacement of existing equipment?',
        'sorting' : 3
    }