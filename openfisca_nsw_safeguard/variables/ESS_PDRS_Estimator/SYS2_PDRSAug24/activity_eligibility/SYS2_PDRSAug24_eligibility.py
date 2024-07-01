from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class SYS2_PDRSAug24_replacement_final_activity_eligibility(Variable):
    """
        Formula to calculate the SYS2 replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        replacement_existing_equipment_removed = buildings('SYS2_PDRSAug24_replacement_existing_equipment_removed', period)
        new_equipment_installed_on_site = buildings('SYS2_PDRSAug24_equipment_installed_on_site', period)
        qualified_install_removal = buildings('SYS2_PDRSAug24_qualified_install_removal', period)
        ACP_engaged = buildings('SYS2_PDRSAug24_engaged_ACP', period)
        registered_GEMS = buildings('SYS2_PDRSAug24_equipment_registered_in_GEMS', period)
        star_rating_minimum_four = buildings('SYS2_PDRSAug24_star_rating_minimum_four', period)
        warranty = buildings('SYS2_PDRSAug24_warranty', period)

        end_formula = ( replacement_existing_equipment_removed * new_equipment_installed_on_site * qualified_install_removal * ACP_engaged *
                        registered_GEMS * star_rating_minimum_four * warranty )

        return end_formula