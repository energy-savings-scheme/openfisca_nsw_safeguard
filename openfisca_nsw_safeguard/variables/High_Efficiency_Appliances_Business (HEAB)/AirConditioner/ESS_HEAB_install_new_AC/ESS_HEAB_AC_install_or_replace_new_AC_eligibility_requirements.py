from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

from openfisca_nsw_safeguard.variables.ESS_general.ESS_BCA_climate_zone import BCA_building_class


class ESS_HEAB_install_or_replace_AC_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Eligibility' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC install meets eligibility requirements",
    }

    def formula(buildings, period, parameters):
        BCA_building_class = buildings('BCA_building_class', period)
        BuildingClass = BCA_building_class.possible_values

        activity_type = buildings('PDRS_activity_type', period)
        ActivityType = activity_type.possible_values
        is_install_AC = (activity_type == ActivityType.install_AC)
        is_replace_AC = (activity_type == ActivityType.replace_AC)
        is_residential = (
                            (BCA_building_class == BuildingClass.BCA_Class_1a) +
                            (BCA_building_class == BuildingClass.BCA_Class_1b) +
                            (BCA_building_class == BuildingClass.BCA_Class_2) +
                            (BCA_building_class == BuildingClass.BCA_Class_4)
        )
        return (
            (is_install_AC + is_replace_AC) *
            np.logical_not(is_residential)
        )
