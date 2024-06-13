from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class RF2_F1_2_ESSJun24_installation_replacement_final_activity_eligibility(Variable):
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
        eligible_display_sides = buildings('RF2_F1_2_ESSJun24_display_sides_eligible', period)
        registered_GEMS = buildings('RF2_F1_2_ESSJun24_equipment_registered_in_GEMS', period)
        product_class_5 = buildings('RF2_F1_2_ESSJun24_GEMS_product_class_5', period)

      
        #if product class is 5 then EEI must be below 51 otherwise for all other product classes EEI must be below 81
        EEI_under_51 = buildings('RF2_F1_2_ESSJun24_EEI_under_51', period)
        EEI_under_81 = buildings('RF2_F1_2_ESSJun24_EEI_under_81', period)

        EEI_eligible_by_product_class = (product_class_5 * EEI_under_51) + (np.logical_not(product_class_5) * EEI_under_81)
 
        end_formula = ( replacement * same_product_class * qualified_install_removal *
                        legal_disposal * ACP_engaged * minimum_payment * installed_on_site * eligible_display_sides * 
                        registered_GEMS * EEI_eligible_by_product_class )

        return end_formula