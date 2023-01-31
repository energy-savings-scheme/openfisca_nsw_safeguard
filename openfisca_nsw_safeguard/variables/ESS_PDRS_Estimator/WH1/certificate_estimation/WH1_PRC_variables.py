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
        'sorting' : 9,
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
    
    def formula(building, period, parameters):
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
        "alias": "Zone"
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
        'variable-type' : 'user-input',
        'alias' : 'PDRS Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1,
        'label': 'Postcode'
    }


class WH1_BCA_climate_zone_by_postcode(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    metadata={
        'variable-type' : 'inter-interesting'
    }

    def formula(buildings, period, parameters):
        postcode = buildings('WH1_PDRS__postcode', period)
        # Returns an integer
        climate_zone = parameters(period).ESS.ESS_general.table_A26_BCA_climate_zone_by_postcode       
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


class WH1_get_network_loss_factor_by_postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }
    def formula(building, period, parameters):
        postcode = building('WH1_PDRS__postcode', period)
        network_loss_factor = parameters(period).PDRS.table_network_loss_factor_by_postcode[postcode]

        return network_loss_factor


class WH1_annual_energy_savings_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    default_value = False

    def formula(buildings, period, parameters):

        minimum_savings = buildings('WH1_annual_energy_savings', period)
        heat_pump_zone = buildings('WH1_get_zone_by_postcode', period)
        BCA_climate_zone = buildings('WH1_BCA_climate_zone_by_postcode', period)

        minimum_savings_by_HP_zone_to_check = np.select(
            [
                minimum_savings < 60,
                (minimum_savings >= 60) * (heat_pump_zone == 5) * (BCA_climate_zone == 'BCA_Climate_Zone_1'), 
                (minimum_savings >= 60) * (heat_pump_zone == 5) * (BCA_climate_zone == 'BCA_Climate_Zone_2'), 
                (minimum_savings >= 60) * (heat_pump_zone == 5) * (BCA_climate_zone == 'BCA_Climate_Zone_3'), 
                (minimum_savings >= 60) * (heat_pump_zone == 5) * (BCA_climate_zone == 'BCA_Climate_Zone_4'), 
                (minimum_savings >= 60) * (heat_pump_zone == 5) * (BCA_climate_zone == 'BCA_Climate_Zone_5'), 
                (minimum_savings >= 60) * (heat_pump_zone == 5) * (BCA_climate_zone == 'BCA_Climate_Zone_6'), 
                (minimum_savings >= 60) * (heat_pump_zone == 5) * (BCA_climate_zone == 'BCA_Climate_Zone_7'),
                (minimum_savings >= 60) * (heat_pump_zone == 5) * (BCA_climate_zone == 'BCA_Climate_Zone_8'),
                (minimum_savings >= 60) * (heat_pump_zone == 3) * (BCA_climate_zone == 'BCA_Climate_Zone_1'),
                (minimum_savings >= 60) * (heat_pump_zone == 3) * (BCA_climate_zone == 'BCA_Climate_Zone_2'),
                (minimum_savings >= 60) * (heat_pump_zone == 3) * (BCA_climate_zone == 'BCA_Climate_Zone_3'),
                (minimum_savings >= 60) * (heat_pump_zone == 3) * (BCA_climate_zone == 'BCA_Climate_Zone_4'),
                (minimum_savings >= 60) * (heat_pump_zone == 3) * (BCA_climate_zone == 'BCA_Climate_Zone_5'),
                (minimum_savings >= 60) * (heat_pump_zone == 3) * (BCA_climate_zone == 'BCA_Climate_Zone_6'),
                (minimum_savings >= 60) * (heat_pump_zone == 3) * (BCA_climate_zone == 'BCA_Climate_Zone_7'),
                (minimum_savings >= 60) * (heat_pump_zone == 3) * (BCA_climate_zone == 'BCA_Climate_Zone_8')
            ],
            [
                False,
                False,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                True,
                True
            ])

        return minimum_savings_by_HP_zone_to_check