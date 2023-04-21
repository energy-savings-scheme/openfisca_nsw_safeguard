from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class RF2_installation_replacement_final_activity_eligibility(Variable):
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
        replacement = buildings('RF2_equipment_replaced', period)
        new_installation = buildings('RF2_installation', period)
        qualified_install_removal = buildings('RF2_qualified_install_removal', period)
        legal_disposal = buildings('RF2_legal_disposal', period)
        ACP_engaged = buildings('RF2_engaged_ACP', period)
        registered_GEMS = buildings('RF2_equipment_registered_in_GEMS', period)
        product_class_5 = buildings('RF2_GEMS_product_class_5', period)

        #check if its installation or replacement     
        replacement_or_installation_qualified = np.select([
            (replacement * qualified_install_removal),
            (replacement * np.logical_not(qualified_install_removal)),
            (np.logical_not(replacement) * new_installation * qualified_install_removal),
            (np.logical_not(replacement) * new_installation * np.logical_not(qualified_install_removal))
        ],
        [
            True,
            False,
            False,
            False
        ])

        #if product class is 5 then EEI must be below 51 otherwise for all other product classes EEI must be below 81
        EEI_under_51 = buildings('RF2_EEI_under_51', period)
        EEI_under_81 = buildings('RF2_EEI_under_81', period)

        EEI_eligible_by_product_class = (product_class_5 * EEI_under_51) + (np.logical_not(product_class_5) * EEI_under_81)
 
        end_formula = ( replacement_or_installation_qualified *
                        legal_disposal * ACP_engaged * registered_GEMS *
                        EEI_eligible_by_product_class )

        return end_formula
