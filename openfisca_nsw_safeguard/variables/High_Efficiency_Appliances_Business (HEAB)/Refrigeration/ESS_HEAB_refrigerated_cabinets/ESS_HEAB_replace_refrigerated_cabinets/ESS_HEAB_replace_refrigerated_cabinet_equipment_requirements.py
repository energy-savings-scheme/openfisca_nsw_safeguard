from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

import numpy as np


class ESS_HEAB_replace_refrigerated_cabinet_is_under_baseline_EEI(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the refrigerated cabinet stay under the baseline EEI?'
    metadata = {
        'alias':  'The existing equipment is classified as a refrigerator',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        product_class = buildings('refrigerated_cabinet_product_class', period)
        RCProductClass = product_class.possible_values
        new_product_EEI = buildings('new_refrigerated_cabinet_EEI', period)
        is_class_5_product = (
            product_class == RCProductClass.product_class_five
        )
        return np.where(is_class_5_product,
                            new_product_EEI < 51,
                            new_product_EEI < 81)



class ESS_HEAB_replace_refrigerated_cabinet_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet the Equipment Requirements defined in Activity Definition F1?'
    metadata = {
        'alias':  'The existing equipment is classified as a refrigerator',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        is_refrigerated_cabinet = buildings(
            'ESS_HEAB_new_equipment_is_RC', period)
        is_under_baseline_EEI = buildings(
            'ESS_HEAB_replace_refrigerated_cabinet_is_under_baseline_EEI', period)
        is_registered_in_GEMS = buildings(
            'ESS_HEAB_refrigerated_cabinet_is_registered_in_GEMS', period)
        return(
                is_refrigerated_cabinet *
                is_under_baseline_EEI * 
                is_registered_in_GEMS
                )