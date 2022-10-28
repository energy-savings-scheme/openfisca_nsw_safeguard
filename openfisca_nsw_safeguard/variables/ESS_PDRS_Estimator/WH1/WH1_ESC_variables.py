import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for WH1 ESC Calculation
    These variables use VEU Registry data
"""
class WH1_HP_capacity_factor(Variable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Total rated capacity of the heat pump water heater(s) being installed',
        'sorting' : 3
    }


class WH1_WH_capacity_factor(Variable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Total rated capacity (kW) of the End-User Equipment being replaced',
        'sorting' : 4
    }


class WH1_HP_gas(Variable):
    reference = 'GJ per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Annual gas energy used by the End-User Equipment',
        'sorting' : 5
    }


class WH1_com_peak_load(Variable):
    reference = 'MJ per day'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    
    metadata = {
        'display_question': 'Peak daily (winter) load based on the address of the site where the End-User Equipment is installed',
        'sorting' : 6
    }


class WH1_HP_elec(Variable):
    reference = 'GJ per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    
    metadata = {
        'display_question': 'Annual electrical energy used by the End-User Equipment',
        'sorting' : 7
    }


""" These variables use Rule tables
"""

class WH1_regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor from ESS Table A24'
    
    def formula(buildings, period, parameters):
        postcode = buildings('WH1_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)
