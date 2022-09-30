from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class PDRS__HVAC2_installation_final_activity_eligibility(Variable):
    """
        Formula to calculate the HVAC2 installation activity eligibility
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
        new_installation = buildings('PDRS_HVAC_2_installation', period)
        qualified_install = buildings('Implementation_is_performed_by_qualified_person', period)
        equipment_installed = buildings('Equipment_is_installed', period)
        residential_building = buildings('PDRS__residential_building', period)
        registered_GEMS = buildings('HVAC2_appliance_is_registered_in_GEMS', period)
        cooling_capacity = buildings('new_AC_cooling_capacity', period)
        TCPSF_greater = buildings('HVAC_2_TCPSF_greater_than_minimum', period)
        is_installed_in_class_2 = buildings('is_installed_centralised_system_common_area_BCA_Class2_building', period)

        climate_zone = buildings('AC_climate_zone', period)
        ACClimateZone = climate_zone.possible_values
        in_average_zone = (climate_zone == ACClimateZone.average_zone) # True
        in_hot_zone = (climate_zone == ACClimateZone.hot_zone) # False
        in_cold_zone = (climate_zone == ACClimateZone.cold_zone) # False
        
        heating_capacity = buildings('new_AC_heating_capacity', period)
        HSPF_mixed_value = buildings('AC_HSPF_mixed', period)
        HSPF_cold_value = buildings('AC_HSPF_cold', period)
        AEER_greater_than_minimum = buildings('HVAC_2_AEER_greater_than_minimum',period)
        ACOP_value = buildings ('AC_ACOP', period)
        
        # residential building is NO or residential building is yes and is installed in BCA class 2
        residential_building_with_class_2 = np.logical_not(residential_building) + (residential_building * is_installed_in_class_2)
        
        # GEMS cooling capacity is NO but AEER greater than minimum YES OR  GEMS cooling capacity is YES and TCPSF_greater greater than minimum YES
        gems_cooling_capacity_path = (np.logical_not(cooling_capacity) * AEER_greater_than_minimum) + (cooling_capacity * TCPSF_greater)
        
        hot_zone_intermediary = in_hot_zone * ((heating_capacity * HSPF_mixed_value) + (np.logical_not(heating_capacity) * ACOP_value))
        average_zone_intermediary = in_average_zone * ((heating_capacity * HSPF_mixed_value) + (np.logical_not(heating_capacity) * ACOP_value))
        cool_zone_intermediary = in_cold_zone * ( (heating_capacity * HSPF_cold_value) + (np.logical_not(heating_capacity) * ACOP_value))
        
        climate_zone_condition = hot_zone_intermediary + average_zone_intermediary + cool_zone_intermediary
        
        end_formula =  ( new_installation * qualified_install * equipment_installed * 
                    residential_building_with_class_2 * registered_GEMS * gems_cooling_capacity_path * climate_zone_condition )
        
        return end_formula
    
    
class PDRS__HVAC2_replacement_final_activity_eligibility(Variable):
    """
        Formula to calculate the HVAC2 installation activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the requirements of the HVAC2 Activity?'
    metadata = {
        "alias": "HVAC2 activity replacement eligibility requirements",
        "variable-type": "output"
    }
    
    def formula(buildings, period, parameter):
        replacement = buildings('PDRS_HVAC_2_replacement', period)
        qualified_install = buildings('Implementation_is_performed_by_qualified_person', period)
        qualified_removal_replacement = buildings('Equipment_is_removed', period)
        residential_building = buildings('PDRS__residential_building', period)
        registered_GEMS = buildings('HVAC2_appliance_is_registered_in_GEMS', period)
        cooling_capacity = buildings('new_AC_cooling_capacity', period)
        TCPSF_greater = buildings('HVAC_2_TCPSF_greater_than_minimum', period)
        is_installed_in_class_2 = buildings('is_installed_centralised_system_common_area_BCA_Class2_building', period)

        climate_zone = buildings('AC_climate_zone', period)
        ACClimateZone = climate_zone.possible_values
        in_average_zone = (climate_zone == ACClimateZone.average_zone) # True
        in_hot_zone = (climate_zone == ACClimateZone.hot_zone) # False
        in_cold_zone = (climate_zone == ACClimateZone.cold_zone) # False
        
        heating_capacity = buildings('new_AC_heating_capacity', period)
        HSPF_mixed_value = buildings('AC_HSPF_mixed', period)
        HSPF_cold_value = buildings('AC_HSPF_cold', period)
        AEER_greater_than_minimum = buildings('HVAC_2_AEER_greater_than_minimum',period)
        ACOP_value = buildings ('AC_ACOP', period)
        
        
        # residential building is NO or residential building is yes and is installed in BCA class 2
        residential_building_with_class_2 = np.logical_not(residential_building) + (residential_building * is_installed_in_class_2)
        
        # GEMS cooling capacity is NO but AEER greater than minimum YES OR  GEMS cooling capacity is YES and TCPSF_greater greater than minimum YES
        gems_cooling_capacity_path = (np.logical_not(cooling_capacity) * AEER_greater_than_minimum) + (cooling_capacity * TCPSF_greater)
        
        
        hot_zone_intermediary = in_hot_zone * (heating_capacity * HSPF_mixed_value) + (np.logical_not(heating_capacity) * ACOP_value)
        average_zone_intermediary = in_average_zone * (heating_capacity * HSPF_mixed_value) + (np.logical_not(heating_capacity) * ACOP_value)
        cool_zone_intermediary = in_cold_zone * (heating_capacity * HSPF_cold_value) + (np.logical_not(heating_capacity) * ACOP_value)
        
        end_formula =  ( replacement * qualified_install * qualified_removal_replacement * 
                    residential_building_with_class_2 * registered_GEMS * gems_cooling_capacity_path * 
                        ( hot_zone_intermediary + average_zone_intermediary + cool_zone_intermediary ) )
        
        return end_formula
