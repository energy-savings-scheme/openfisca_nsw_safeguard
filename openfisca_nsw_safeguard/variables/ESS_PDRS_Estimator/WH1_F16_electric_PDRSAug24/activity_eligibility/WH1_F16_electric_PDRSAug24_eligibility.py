from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

class WH1_F16_electric_PDRSAug24__installation_replacement_final_activity_eligibility(Variable):
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
        replacement = buildings('WH1_F16_electric_PDRSAug24__equipment_replaced', period)
        existing_equipment_removed = buildings('WH1_F16_electric_PDRSAug24__existing_equipment_removed', period)
        equipment_installed_on_site = buildings('WH1_F16_electric_PDRSAug24__equipment_installed_on_site', period)
        qualified_install_removal = buildings('WH1_F16_electric_PDRSAug24__qualified_install_removal', period)
        engaged_ACP = buildings('WH1_F16_electric_PDRSAug24__engaged_ACP', period)
        minimum_payment = buildings('WH1_F16_electric_PDRSAug24__minimum_payment', period)
        not_class_1_or_4 = buildings('WH1_F16_electric_PDRSAug24__building_BCA_not_class_1_or_4', period)
        certified_4234 = buildings('WH1_F16_electric_PDRSAug24__4234_certified', period)
        scheme_admin_approved = buildings('WH1_F16_electric_PDRSAug24__scheme_admin_approved', period)
        minimum_annual_energy = buildings('WH1_F16_electric_PDRSAug24__minimum_annual_energy', period)
        storage_volume_certified = buildings('WH1_F16_electric_PDRSAug24__equipment_certified_by_storage_volume', period)
        

        end_formula = ( replacement * existing_equipment_removed * equipment_installed_on_site * qualified_install_removal 
                        * engaged_ACP * minimum_payment * certified_4234 * scheme_admin_approved * minimum_annual_energy
                        * np.logical_not(not_installed_class_1_or_4) * storage_volume_certified )

        return end_formula