from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import ESS_2021


class ESS_PDRS_is_residential(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Site is located in a residential building?'
    metadata = {
        'alias':  'Site is located in a residential building?',
        "regulation_reference": ESS_2021["XX", "GA"]
    }

    def formula(buildings, period, parameters):
        BCA_building_class = buildings('BCA_building_class', period)
        BCABuildingClass = BCA_building_class.possible_values

        is_residential = (
                (BCA_building_class == BCABuildingClass.BCA_Class_1a) +
                (BCA_building_class == BCABuildingClass.BCA_Class_1b) +
                (BCA_building_class == BCABuildingClass.BCA_Class_2) +
                (BCA_building_class == BCABuildingClass.BCA_Class_4)
        )
        return is_residential


class Appliance_located_in_small_business_building(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Site is located in a small business building?'
    metadata = {
        'alias':  'Site is located in a small business building?',
        "regulation_reference": ESS_2021["XX", "GA"]
    }