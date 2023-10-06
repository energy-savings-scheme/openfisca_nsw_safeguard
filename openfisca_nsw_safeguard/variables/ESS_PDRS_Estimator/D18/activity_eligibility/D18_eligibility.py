from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class D18_replacement_final_activity_eligibility(Variable):
    """
        Formula to calculate the D18 replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "D18 activity installation eligibility requirements",
        "variable-type": "output"
    }
    
    def formula(buildings, period, parameter):
        equipment_replaced = buildings('D18_equipment_replaced', period)
        replaces_electric = buildings('D18_equipment_replaces_electric', period)
        ACP_engaged = buildings('D18_engaged_ACP', period)
        equipment_removed = buildings('D18_equipment_removed', period)
        new_equipment_installed = buildings('D18_equipment_installed', period)
        qualified_install = buildings('D18_installed_by_qualified_person', period)
        registered_IPART = buildings('D18_equipment_registered_IPART', period)
        
        end_formula =  ( equipment_replaced * replaces_electric * ACP_engaged *
                        equipment_removed * new_equipment_installed * qualified_install * registered_IPART)
        
        return end_formula