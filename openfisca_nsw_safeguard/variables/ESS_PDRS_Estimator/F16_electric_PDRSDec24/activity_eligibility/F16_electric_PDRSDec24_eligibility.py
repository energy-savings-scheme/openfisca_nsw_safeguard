from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

class F16_electric_PDRSDec24__installation_replacement_final_activity_eligibility(Variable):
    """
        Formula to calculate the WH1 replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        replacement = buildings('F16_electric_PDRSDec24__equipment_replaced', period)
        existing_equipment_removed = buildings('F16_electric_PDRSDec24__existing_equipment_removed', period)
        equipment_installed_on_site = buildings('F16_electric_PDRSDec24__equipment_installed_on_site', period)
        qualified_install_removal = buildings('F16_electric_PDRSDec24__qualified_install_removal', period)
        engaged_ACP = buildings('F16_electric_PDRSDec24__engaged_ACP', period)
        minimum_payment = buildings('F16_electric_PDRSDec24__minimum_payment', period)
        building_class_1_or_4 = buildings('F16_electric_PDRSDec24__building_BCA_class_1_or_4', period)
        certified_4234 = buildings('F16_electric_PDRSDec24__4234_certified', period)
        minimum_annual_energy = buildings('F16_electric_PDRSDec24__minimum_annual_energy', period)
        storage_volume_certified = buildings('F16_electric_PDRSDec24__certified_and_eligible', period)
        safety_requirement = buildings('F16_electric_PDRSDec24__safety_requirement', period)

        end_formula = ( replacement * existing_equipment_removed * equipment_installed_on_site * qualified_install_removal
                        * engaged_ACP * minimum_payment * certified_4234 * minimum_annual_energy
                        * np.logical_not(building_class_1_or_4) * storage_volume_certified *  safety_requirement)

        return end_formula