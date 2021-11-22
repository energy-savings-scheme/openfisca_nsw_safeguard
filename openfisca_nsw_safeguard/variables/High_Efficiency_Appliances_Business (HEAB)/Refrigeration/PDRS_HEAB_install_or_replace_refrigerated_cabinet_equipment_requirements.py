from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

class PDRS_HEAB_install_or_replace_refrigerated_cabinet_activity_new_equipment_is_RC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a Refrigerated Cabinet?'
    metadata = {
        'alias':  'The existing equipment is classified as a refrigerator',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }


class PDRS_HEAB_install_or_replace_refrigerated_cabinet_is_under_baseline_EEI(Variable):
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
        new_RC_EEI = buildings('new_refrigerated_cabinet_EEI', period)
        baseline_EEI = parameters(period).PDRS.refrigerated_cabinets.PDRS_refrigerated_cabinets_EEI_baselines[product_class]
        return (new_RC_EEI < baseline_EEI)

class PDRS_HEAB_install_or_replace_refrigerated_cabinet_is_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new refrigerated cabinet registered in the GEMS Registry?'
    metadata = {
        'alias':  'The existing equipment is classified as a refrigerator',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }


class PDRS_HEAB_install_or_replace_refrigerated_cabinet_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet the Equipment Requirements defined in Activity Definition F1?'
    metadata = {
        'alias':  'The existing equipment is classified as a refrigerator',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        is_refrigerated_cabinet = buildings('PDRS_HEAB_install_or_replace_refrigerated_cabinet_activity_new_equipment_is_RC', period)
        is_under_baseline_EEI = buildings('PDRS_HEAB_install_or_replace_refrigerated_cabinet_is_under_baseline_EEI', period)
        is_registered_in_GEMS = buildings('PDRS_HEAB_install_or_replace_refrigerated_cabinet_is_registered_in_GEMS', period)
        return(
                is_refrigerated_cabinet *
                is_under_baseline_EEI * 
                is_registered_in_GEMS
                )