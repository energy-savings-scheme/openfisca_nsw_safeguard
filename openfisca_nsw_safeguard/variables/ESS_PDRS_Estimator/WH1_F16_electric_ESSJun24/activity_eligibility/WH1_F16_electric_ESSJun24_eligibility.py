from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

class WH1_F16_electric_ESSJun24__installation_replacement_final_activity_eligibility(Variable):
    """
        Formula to calculate the WH1 installation/replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        replacement = buildings('WH1_F16_electric_ESSJun24__equipment_replaced', period)
        qualified_removal_install = buildings('WH1_F16_electric_ESSJun24__equipment_removed', period)
        ACP_engaged = buildings('WH1_F16_electric_ESSJun24__engaged_ACP', period)
        minimum_payment = buildings('WH1_F16_electric_ESSJun24__minimum_payment', period)
        not_installed_class_1_or_4 = buildings('WH1_F16_electric_ESSJun24__building_BCA_not_class_1_or_4', period)
        scheme_admin_approved = buildings('WH1_F16_electric_ESSJun24__scheme_admin_approved', period)
        storage_volume_certified = buildings('WH1_F16_electric_ESSJun24__equipment_certified_by_storage_volume', period)
        

        end_formula = ( replacement * qualified_removal_install * ACP_engaged * minimum_payment
                        * np.logical_not(not_installed_class_1_or_4) * scheme_admin_approved 
                        * storage_volume_certified )

        return end_formula