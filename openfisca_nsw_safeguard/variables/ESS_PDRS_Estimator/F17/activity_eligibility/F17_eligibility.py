from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

class F17_installation_final_activity_eligibility(Variable):
    """
        Formula to calculate the F17 installation activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        new_installation = buildings('F17_equipment_new_installation', period)
        recognised_certification = buildings('F17_4234_certified', period)
        qualified_install = buildings('F17_installed_by_qualified_person', period)
        ACP_engaged = buildings('F17_engaged_ACP', period)
        minimum_payment = buildings('F17_minimum_payment', period)
        not_installed_class_1_or_4 = buildings('F17_building_BCA_not_class_1_or_4', period)        
        storage_volume_certified = buildings('F17_equipment_certified_by_storage_volume', period)
        split_system = buildings('F17_split_system', period)
        safety_requirement = buildings('F17_safety_requirement', period)
        
        end_formula = ( new_installation * recognised_certification * qualified_install * ACP_engaged * minimum_payment * np.logical_not(not_installed_class_1_or_4) * 
                        storage_volume_certified * safety_requirement)

        return end_formula
