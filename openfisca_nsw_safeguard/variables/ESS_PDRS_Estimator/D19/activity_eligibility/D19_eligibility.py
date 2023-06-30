from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class D19_replacement_final_activity_eligibility(Variable):
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
        equipment_replaced = buildings('D19_equipment_replaced', period)
        replaces_gas = buildings('D19_equipment_replaces_gas', period)
        ACP_engaged = buildings('D19_engaged_ACP', period)
        equipment_removed = buildings('D19_equipment_removed', period)
        new_equipment_installed = buildings('D19_equipment_installed', period)
        qualified_install = buildings('D19_installed_by_qualified_person', period)
        registered_GEMS = buildings('D19_equipment_registered_IPART', period)
        
        end_formula =  ( equipment_replaced * replaces_gas * ACP_engaged *
                        equipment_removed * new_equipment_installed * qualified_install * registered_GEMS)
        
        return end_formula