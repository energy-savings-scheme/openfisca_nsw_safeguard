from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building
import numpy as np


class RF2_F1_2_ESSJun24_installation_replacement_final_activity_eligibility(BaseVariable):
    """
        Formula to calculate the RF2 installation/replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameter):
        replacement = buildings('RF2_F1_2_ESSJun24_equipment_replaced', period)
        same_product_class = buildings('RF2_F1_2_ESSJun24_same_product_class', period)
        qualified_install_removal = buildings('RF2_F1_2_ESSJun24_qualified_install_removal', period)
        legal_disposal = buildings('RF2_F1_2_ESSJun24_legal_disposal', period)
        ACP_engaged = buildings('RF2_F1_2_ESSJun24_engaged_ACP', period)
        minimum_payment = buildings('RF2_F1_2_ESSJun24_minimum_payment', period)
        installed_on_site = buildings('RF2_F1_2_ESSJun24_installed_on_site', period)
        eligible_display_sides = buildings('RF2_F1_2_ESSJun24_display_sides', period)
        registered_GEMS = buildings('RF2_F1_2_ESSJun24_equipment_registered_in_GEMS', period)
        product_class_12 = buildings('RF2_F1_2_ESSJun24_GEMS_product_class_12', period)
        EEI_under_77 = buildings('RF2_F1_2_ESSJun24_EEI_under_77', period)
        EEI_under_81 = buildings('RF2_F1_2_ESSJun24_EEI_under_81', period)
        # We didnt include replacement variable because both installation and replacement are now eligibile.
        end_formula = ( same_product_class * qualified_install_removal *
                        legal_disposal * ACP_engaged * minimum_payment * installed_on_site * eligible_display_sides * 
                        registered_GEMS * product_class_12 * EEI_under_77 * EEI_under_81 )

        return end_formula