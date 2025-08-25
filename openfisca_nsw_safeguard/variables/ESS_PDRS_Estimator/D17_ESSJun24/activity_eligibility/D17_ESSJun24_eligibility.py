from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class D17_ESSJun24_replacement_final_activity_eligibility(Variable):
    """
        Formula to calculate the D17 replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "D17 activity installation eligibility requirements",
        "variable-type": "output"
    }
    
    def formula(buildings, period, parameter):
        equipment_replaced = buildings('D17_ESSJun24_equipment_replaced', period)
        ACP_engaged = buildings('D17_ESSJun24_engaged_ACP', period)
        minimum_payment = buildings('D17_ESSJun24_minimum_payment', period)
        equipment_removed = buildings('D17_ESSJun24_equipment_removed', period)
        new_equipment_installed = buildings('D17_ESSJun24_equipment_installed', period)
        qualified_install = buildings('D17_ESSJun24_installed_by_qualified_person', period)
        registered_IPART = buildings('D17_ESSJun24_equipment_registered_IPART', period)
        split_system = buildings('D17_ESSJun24_split_system', period)
        safety_requirement = buildings('D17_ESSJun24_safety_requirement', period)
        
        end_formula =  ( equipment_replaced * ACP_engaged * minimum_payment *
                        equipment_removed * new_equipment_installed * qualified_install * registered_IPART * safety_requirement )
        
        return end_formula