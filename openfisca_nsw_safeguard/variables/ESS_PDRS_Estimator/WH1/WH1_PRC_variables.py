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

class WH1_annual_energy_savings(Variable):
    reference = 'Percentage'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual energy savings (%/year)'
    metadata = {
        'display_question': 'Annual energy savings as a percentage per year',
        'sorting' : 8,
        'variable-type': 'input',
        'label': 'Annual energy savings (%/year)'
    }


""" These variables use Rule tables
"""
class network_loss_factor_options(Enum):
    Ausgrid = 'Ausgrid'
    Endeavour = 'Endeavour'
    Essential = 'Essential'


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
        "display_question": "Who is your network service provider?",
        'sorting' : 2
    }


class WH1_get_zone_by_postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "Zone",
    }
    def formula(building, period, parameters):
        postcode = building('WH1_PDRS__postcode', period)
        zones = parameters(period).ESS.ESS_general.Postcode_zones_air_source_heat_pumps
        return zones.calc(postcode)
    

class WH1_PDRS__postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = "What is the postcode for the building you are calculating PRCs for?"
    metadata={
        'alias' : 'PDRS Postcode',
        'display_question' : 'Based on your postcode',
        'sorting' : 1,
        'label': "The postcode for the building you are calculating PRCs for"
        }