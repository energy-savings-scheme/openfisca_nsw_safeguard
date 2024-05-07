from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class D19_ESSJun24_replacement_final_activity_eligibility(Variable):
    """
        Formula to calculate the D19 replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "D19 activity installation eligibility requirements",
        "variable-type": "output"
    }
    
    def formula(buildings, period, parameter):
        equipment_replaced = buildings('D19_ESSJun24_equipment_replaced', period)
        ACP_engaged = buildings('D19_ESSJun24_engaged_ACP', period)
        minimum_payment = buildings('D19_ESSJun24_minimum_payment', period)
        equipment_removed = buildings('D19_ESSJun24_equipment_removed', period)
        new_equipment_installed = buildings('D19_ESSJun24_equipment_installed', period)
        qualified_install = buildings('D19_ESSJun24_installed_by_qualified_person', period)
        registered_IPART = buildings('D19_ESSJun24_equipment_registered_IPART', period)
        
        end_formula =  ( equipment_replaced * ACP_engaged * minimum_payment *
                        equipment_removed * new_equipment_installed * qualified_install * registered_IPART)
        
        return end_formula