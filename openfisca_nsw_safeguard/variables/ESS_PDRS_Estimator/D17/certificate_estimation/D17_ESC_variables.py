from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


""" Parameters for D17 ESC Calculation
    These variables use Rule tables and IPART Registry data
"""


class D17_PDRS__postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata={
        'variable-type' : 'user-input',
        'alias' : 'PDRS Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1,
        'label': 'Postcode'
    }


class D17_get_zone_by_postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "Zone"
    }
    def formula(building, period, parameters):
        postcode = building('D17_PDRS__postcode', period)
        zones = parameters(period).ESS.ESS_general.Postcode_zones_air_source_heat_pumps
        return zones.calc(postcode)
    

class D17_regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor from ESS Table A24'
    
    def formula(buildings, period, parameters):
        postcode = buildings('D17_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)


class D17_replacement_activity(Variable):
    value_type = bool
    default_value = True
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'user-input',
        'label': 'Replacement or new installation activity',
        'display_question': 'Is the activity the replacement of existing equipment?',
        'sorting' : 2
    }


class D17_System_Size(Enum):
    system_size_small = 'small'
    system_size_medium = 'medium'


class D17_system_size(Variable):
    value_type = Enum
    entity = Building
    definition_period = ETERNITY
    possible_values = D17_System_Size
    default_value = D17_System_Size.system_size_small
    metadata = {
      'variable-type': 'user-input',
      'label': 'System Size',
      'display_question' : 'Thermal peak load size',
      'sorting' : 3
    }


class D17_system_size_int(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
        system_size = buildings('D17_system_size', period)
        system_size_int = np.select(
            [
                (system_size == D17_System_Size.system_size_small),
                (system_size == D17_System_Size.system_size_medium)
            ],
            [
                'small',
                'medium'
            ])
        return system_size_int


class D17_Baseline_A(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    
    def formula(buildings, period, parameters):
        system_size = buildings('D17_system_size_int', period)

        baseline_A = parameters(period).ESS.HEER.table_D17_1['baseline_energy_consumption'][system_size]
        return baseline_A
  

class D17_Bs(Variable):
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Annual supplementary energy used by the installed End-User Equipment',
        'sorting' : 4,
        'label': 'Bs (GJ/year)',
        'variable-type': 'input'
    }


class D17_Be(Variable):
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Annual electrical energy used by the auxiliary equipment',
        'sorting' : 4,
        'label': 'Be (GJ/year)',
        'variable-type': 'input'
    }