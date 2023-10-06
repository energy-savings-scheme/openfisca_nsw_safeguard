from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class D20_replacement_final_activity_eligibility(Variable):
    """
        Formula to calculate the D20 replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "D20 activity installation eligibility requirements",
        "variable-type": "output"
    }
    
    def formula(buildings, period, parameter):
        equipment_replaced = buildings('D20_equipment_replaced', period)
        replaces_gas = buildings('D20_equipment_replaces_gas', period)
        ACP_engaged = buildings('D20_engaged_ACP', period)
        equipment_removed = buildings('D20_equipment_removed', period)
        new_equipment_installed = buildings('D20_equipment_installed', period)
        qualified_install = buildings('D20_installed_by_qualified_person', period)
        registered_IPART = buildings('D20_equipment_registered_IPART', period)
        
        end_formula =  ( equipment_replaced * replaces_gas * ACP_engaged *
                        equipment_removed * new_equipment_installed * qualified_install * registered_IPART)
        
        return end_formula