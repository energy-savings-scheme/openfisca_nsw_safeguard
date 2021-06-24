from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

class ESS_BCAClimateZone(Enum):
    BCA_climate_zone_1 = 'Activity takes place in BCA Climate Zone 1.'
    BCA_climate_zone_2 = 'Activity takes place in BCA Climate Zone 2.'
    BCA_climate_zone_3 = 'Activity takes place in BCA Climate Zone 3.'
    BCA_climate_zone_4 = 'Activity takes place in BCA Climate Zone 4.'
    BCA_climate_zone_5 = 'Activity takes place in BCA Climate Zone 5.'
    BCA_climate_zone_6 = 'Activity takes place in BCA Climate Zone 6.'
    BCA_climate_zone_7 = 'Activity takes place in BCA Climate Zone 7.'
    BCA_climate_zone_8 = 'Activity takes place in BCA Climate Zone 8.'


class ESS__BCA_climate_zone(Variable):
    value_type = Enum
    entity = Building
    possible_values = ESS_BCAClimateZone
    default_value = ESS_BCAClimateZone.BCA_climate_zone_2
    definition_period = ETERNITY
    label = 'What BCA climate zone is the activity taking place in?'
    metadata={
        "variable-type": "user-input",
        "alias":"ESS BCA Climate Zone",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Energy Savings Scheme - General'
        }
