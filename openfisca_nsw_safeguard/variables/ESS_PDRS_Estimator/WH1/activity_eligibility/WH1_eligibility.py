from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

class WH1_installation_replacement_final_activity_eligibility(Variable):
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
        replacement = buildings('WH1_equipment_replaced', period)
        new_installation = buildings('WH1_installation', period)
        electric_replacement = buildings('WH1_equipment_replaces_electric', period)
        qualified_removal_install = buildings('WH1_equipment_removed', period)
        equipment_installed = buildings('WH1_equipment_installed_and_operational', period)
        not_installed_class_1_or_4 = buildings('WH1_building_BCA_not_class_1_or_4', period)
        air_source_heat_pump = buildings('WH1_air_source_heat_pump', period)
        scheme_admin_approved = buildings('WH1_scheme_admin_approved', period)
        minimum_savings_met = buildings('WH1_minimum_savings', period)
        storage_volume_certified = buildings('WH1_equipment_certified_by_storage_volume', period)
        

        #check if its installation or replacement and if replacement, that it's replacing electric
        installation_or_replacement = new_installation + (replacement * electric_replacement)

        end_formula = ( installation_or_replacement * qualified_removal_install * equipment_installed *
                        np.logical_not(not_installed_class_1_or_4) * air_source_heat_pump * scheme_admin_approved *
                        minimum_savings_met * storage_volume_certified )

        return end_formula