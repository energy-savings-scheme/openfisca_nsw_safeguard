from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


""" Parameters for D19 ESC Calculation
    These variables use Rule tables and IPART Registry data
"""


class D19_PDRS__postcode(Variable):
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


class D19_BCA_climate_zone_by_postcode(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    metadata={
        'variable-type' : 'inter-interesting'
    }

    def formula(buildings, period, parameters):
        postcode = buildings('D19_PDRS__postcode', period)
        # Returns an integer
        climate_zone = parameters(period).ESS.ESS_general.table_A26_May25_BCA_climate_zone_by_postcode
        climate_zone_int = climate_zone.calc(postcode)
        BCA_climate_zone_to_check = np.select(
            [
                climate_zone_int == 1,
                climate_zone_int == 2,
                climate_zone_int == 3,
                climate_zone_int == 4,
                climate_zone_int == 5,
                climate_zone_int == 6,
                climate_zone_int == 7,
                climate_zone_int == 8
            ],
            [
                'BCA_Climate_Zone_1',
                'BCA_Climate_Zone_2',
                'BCA_Climate_Zone_3',
                'BCA_Climate_Zone_4',
                'BCA_Climate_Zone_5',
                'BCA_Climate_Zone_6',
                'BCA_Climate_Zone_7',
                'BCA_Climate_Zone_8'
            ])

        return BCA_climate_zone_to_check
    
    
class D19_BCA_climate_zone_by_postcode_int(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata={
        'variable-type' : 'inter-interesting'
    }

    def formula(buildings, period, parameters):
        postcode = buildings('D19_PDRS__postcode', period)
        # Returns an integer
        climate_zone = parameters(period).ESS.ESS_general.table_A26_May25_BCA_climate_zone_by_postcode
        climate_zone_int = climate_zone.calc(postcode)

        return climate_zone_int
    

class D19_get_HP_zone_by_BCA_climate_zone(Variable): 
    value_type = int
    entity = Building
    definition_period = ETERNITY
    
    def formula(building, period, parameters):
        BCA_climate_zone = building('D19_BCA_climate_zone_by_postcode_int', period)
        heat_pump_zone = parameters(period).ESS.ESS_general.heat_pump_zone_by_BCA_climate_zone
        heat_pump_zone_int = heat_pump_zone.calc(BCA_climate_zone)

        return heat_pump_zone_int
    

class D19_regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor from ESS Table A24'
    
    def formula(buildings, period, parameters):
        postcode = buildings('D19_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)


class D19_replacement_activity(Variable):
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


class D19_System_Size(Enum):
    system_size_small = 'Small'
    system_size_medium = 'Medium'


class D19_system_size(Variable):
    value_type = Enum
    entity = Building
    definition_period = ETERNITY
    possible_values = D19_System_Size
    default_value = D19_System_Size.system_size_small
    metadata = {
      'variable-type': 'user-input',
      'label': 'System Size',
      'display_question' : 'Thermal peak load size',
      'sorting' : 3
    }


class D19_system_size_int(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
        system_size = buildings('D19_system_size', period)
        system_size_int = np.select(
            [
                (system_size == D19_System_Size.system_size_small),
                (system_size == D19_System_Size.system_size_medium)
            ],
            [
                'small',
                'medium'
            ])
        return system_size_int


class D19_Baseline_A(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
        system_size = buildings('D19_system_size_int', period)

        baseline_A = parameters(period).ESS.HEER.table_D19_1['baseline_energy_consumption'][system_size]['baseline_A']
        return baseline_A


class D19_Bs(Variable):
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


class D19_Be(Variable):
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Annual electrical energy used by the auxiliary equipment',
        'sorting' : 5,
        'label': 'Be (GJ/year)',
        'variable-type': 'input'
    }


class D19_Baseline_B(Variable):
    #baseline B is also the deemed activity gas savings value
    value_type = float
    entity = Building
    definition_period = ETERNITY
    
    def formula(buildings, period, parameters):
        system_size = buildings('D19_system_size_int', period)

        baseline_B = parameters(period).ESS.HEER.table_D19_1['baseline_energy_consumption'][system_size]['baseline_B']
        return baseline_B