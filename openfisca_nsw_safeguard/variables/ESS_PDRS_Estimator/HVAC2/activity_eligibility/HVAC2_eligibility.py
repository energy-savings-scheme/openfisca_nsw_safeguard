from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building
import numpy as np


class HVAC2_installation_replacement_final_activity_eligibility(BaseVariable):
    """
        Formula to calculate the HVAC2 installation/replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the requirements of the HVAC2 Activity?'
    metadata = {
        "alias": "HVAC2 activity installation eligibility requirements",
        "variable-type": "output"
    }
    
    def formula(buildings, period, parameter):
        activity_type_eligible = buildings('HVAC2_new_installation_or_replacement_eligible', period)
        qualified_install = buildings('HVAC2_installed_by_qualified_person', period)
        installed_and_operational = buildings('HVAC2_new_ac_installed_and_operational', period)
        minimum_payment = buildings('HVAC2_minimum_payment', period)
        residential_building = buildings('HVAC2_residential_building', period)
        is_installed_in_class_2 = buildings('HVAC2_installed_centralised_system_common_area_BCA_Class2_building', period)
        registered_GEMS = buildings('HVAC2_equipment_registered_in_GEMS', period)
        model_number_GEMS = buildings('HVAC2_model_number_registered_in_GEMS', period)
        multi_split_class = buildings('HVAC2_multi_split_product_class', period)
        outdoor_units = buildings('HVAC2_outdoor_units', period)
        manufacture_approved = buildings('HVAC2_manufacture_approved_GEMS', period)
        cooling_capacity = buildings('HVAC2_new_equipment_cooling_capacity', period)
        TCPSF_greater = buildings('HVAC2_TCPSF_greater_than_minimum', period)

        climate_zone = buildings('HVAC2_climate_zone', period)
        ACClimateZone = climate_zone.possible_values
        in_average_zone = (climate_zone == ACClimateZone.average_zone) # True
        in_hot_zone = (climate_zone == ACClimateZone.hot_zone) # False
        in_cold_zone = (climate_zone == ACClimateZone.cold_zone) # False

        heating_capacity = buildings('HVAC2_new_equipment_heating_capacity', period)
        HSPF_mixed_value = buildings('HVAC2_HSPF_mixed_eligible', period)
        HSPF_cold_value = buildings('HVAC2_HSPF_cold_eligible', period)
        AEER_greater_than_minimum = buildings('HVAC2_AEER_greater_than_minimum',period)
        ACOP_value = buildings ('HVAC2_ACOP_eligible', period)

        # residential building is NO or residential building is yes and is installed in BCA class 2
        residential_building_with_class_2 = np.logical_not(residential_building) + (residential_building * is_installed_in_class_2)

        # Multi split Product class is NO or Multi split Product class is YES and outdoor same manufacturer is YES and system are approved is YES
        outdoor_unit_approval = np.logical_not(multi_split_class) + (multi_split_class * outdoor_units * manufacture_approved)

        # GEMS cooling capacity is NO but AEER greater than minimum YES OR GEMS cooling capacity is YES and TCPSF_greater greater than minimum YES
        gems_cooling_capacity_path = (np.logical_not(cooling_capacity) * AEER_greater_than_minimum) + (cooling_capacity * TCPSF_greater)

        hot_zone_intermediary = in_hot_zone * ((heating_capacity * HSPF_mixed_value) + (np.logical_not(heating_capacity) * ACOP_value))
        average_zone_intermediary = in_average_zone * ((heating_capacity * HSPF_mixed_value) + (np.logical_not(heating_capacity) * ACOP_value))
        cool_zone_intermediary = in_cold_zone * ((heating_capacity * HSPF_cold_value) + (np.logical_not(heating_capacity) * ACOP_value))
        
        climate_zone_condition = hot_zone_intermediary + average_zone_intermediary + cool_zone_intermediary

        end_formula =  ( activity_type_eligible * qualified_install * installed_and_operational  * minimum_payment * 
                        residential_building_with_class_2 * registered_GEMS * model_number_GEMS * outdoor_unit_approval * 
                        gems_cooling_capacity_path * climate_zone_condition )

        return end_formula