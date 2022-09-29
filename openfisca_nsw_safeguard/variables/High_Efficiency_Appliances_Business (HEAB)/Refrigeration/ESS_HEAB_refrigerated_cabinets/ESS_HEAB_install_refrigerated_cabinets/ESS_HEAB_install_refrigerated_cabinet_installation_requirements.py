from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class ESS_HEAB_install_refrigerated_cabinet_new_equipment_is_installed_and_operating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new equipment installed and operating?'
    metadata = {
        'alias':  'The new equipment is installed and operating.',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }


class ESS_HEAB_install_refrigerated_cabinet_meets_installation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet the Implementation Requirements defined in Activity Definition F1?'
    metadata = {
        'alias':  'The existing equipment is classified as a refrigerator',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        new_equipment_installed_and_operating = buildings('ESS_HEAB_install_refrigerated_cabinet_new_equipment_is_installed_and_operating', period)
        performed_by_qualified_person = buildings('Implementation_is_performed_by_qualified_person', period)
        return(
                new_equipment_installed_and_operating * 
                performed_by_qualified_person
                )