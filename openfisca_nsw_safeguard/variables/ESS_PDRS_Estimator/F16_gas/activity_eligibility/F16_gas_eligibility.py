from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

class F16_gas_installation_replacement_final_activity_eligibility(Variable):
    """
        Formula to calculate the F16_gas installation/replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        replacement = buildings('F16_gas_equipment_replaced', period)
        qualified_removal_install = buildings('F16_gas_installed_by_qualified_person', period)
        ACP_engaged = buildings('F16_gas_engaged_ACP', period)
        minimum_payment = buildings('F16_gas_minimum_payment', period)
        not_installed_class_1_or_4 = buildings('F16_gas_building_BCA_not_class_1_or_4', period)
        recognised_certification = buildings('F16_gas_4234_certified', period)
        storage_volume_certified = buildings('F16_gas_equipment_certified_by_storage_volume', period)
        
        end_formula = ( replacement * qualified_removal_install * ACP_engaged *
                        minimum_payment * np.logical_not(not_installed_class_1_or_4) * recognised_certification 
                        * storage_volume_certified )

        return end_formula