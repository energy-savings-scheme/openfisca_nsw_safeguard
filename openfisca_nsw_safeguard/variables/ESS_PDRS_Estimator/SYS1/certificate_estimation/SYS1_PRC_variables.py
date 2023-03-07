from decimal import FloatOperation
import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class SYS1_PDRS__postcode(Variable):
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


class SYS1_get_network_loss_factor_by_postcode(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'input',
        'sorting' : 2,
        'label' : 'Network loss factor is calculated automatically from your postcode. If you have a 0 here, please check your postcode is correct. If the postcode has more than one distribution network service provider, we have chosen the network factor loss with the lowest value.'
    }
    def formula(building, period, parameters):
        postcode = building('SYS1_PDRS__postcode', period)
        network_loss_factor = parameters(period).PDRS.table_network_loss_factor_by_postcode

        return network_loss_factor.calc(postcode)


class SYS1_BCA_climate_zone_by_postcode(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'What BCA climate zone is the activity taking place in?'
    metadata={
        "variable-type": "inter-interesting",
        "alias": "HVAC2 BCA Climate Zone",
    }
    
    def formula(buildings, period, parameters):
        postcode = buildings('SYS1_PDRS__postcode', period)
        # Returns an integer
        climate_zone = parameters(period).ESS.ESS_general.table_A26_BCA_climate_zone_by_postcode       
        climate_zone_int = climate_zone.calc(postcode)
        cooling_capacity_to_check = np.select(
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
                "BCA_Climate_Zone_1",
                "BCA_Climate_Zone_2",
                "BCA_Climate_Zone_3",
                "BCA_Climate_Zone_4",
                "BCA_Climate_Zone_5",
                "BCA_Climate_Zone_6",
                "BCA_Climate_Zone_7",
                "BCA_Climate_Zone_8"
            ])
        return cooling_capacity_to_check