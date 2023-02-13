from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class HVAC1_installation_replacement_final_activity_eligibility(Variable):
    """
        Formula to calculate the HVAC1 installation/replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the requirements of the HVAC1 Activity?'
    metadata = {
        "alias": "HVAC1 activity installation eligibility requirements",
        "variable-type": "output"
    }
    
    def formula(buildings, period, parameter):
        new_installation = buildings('HVAC1_installation', period)
        replacement = buildings('HVAC1_equipment_replaced', period)
        qualified_install = buildings('HVAC1_installed_by_qualified_person', period)
        equipment_installed = buildings('HVAC1_equipment_installed', period)
        registered_GEMS = buildings('HVAC1_equipment_registered_in_GEMS', period)
        cooling_capacity = buildings('HVAC1_new_equipment_cooling_capacity', period)
        TCPSF_greater = buildings('HVAC1_TCPSF_greater_than_minimum', period)
        climate_zone = buildings('HVAC1_climate_zone', period)
        ACClimateZone = climate_zone.possible_values
        in_average_zone = (climate_zone == ACClimateZone.average_zone) # True
        in_hot_zone = (climate_zone == ACClimateZone.hot_zone) # False
        in_cold_zone = (climate_zone == ACClimateZone.cold_zone) # False
        
        heating_capacity = buildings('HVAC1_new_equipment_heating_capacity', period)
        HSPF_mixed_value = buildings('HVAC1_HSPF_mixed_eligible', period)
        HSPF_cold_value = buildings('HVAC1_HSPF_cold_eligible', period)
        AEER_greater_than_minimum = buildings('HVAC1_AEER_greater_than_minimum',period)
        ACOP_value = buildings ('HVAC1_ACOP_eligible', period)
                
        # check if its installation or replacement
        installation_or_replacement = (new_installation * qualified_install) + (replacement * qualified_install)
                
        # GEMS cooling capacity is NO but AEER greater than minimum YES OR GEMS cooling capacity is YES and TCPSF_greater greater than minimum YES
        gems_cooling_capacity_path = (np.logical_not(cooling_capacity) * AEER_greater_than_minimum) + (cooling_capacity * TCPSF_greater)
        
        hot_zone_intermediary = in_hot_zone * ((heating_capacity * HSPF_mixed_value) + (np.logical_not(heating_capacity) * ACOP_value))
        average_zone_intermediary = in_average_zone * ((heating_capacity * HSPF_mixed_value) + (np.logical_not(heating_capacity) * ACOP_value))
        cool_zone_intermediary = in_cold_zone * ((heating_capacity * HSPF_cold_value) + (np.logical_not(heating_capacity) * ACOP_value))
        
        climate_zone_condition = hot_zone_intermediary + average_zone_intermediary + cool_zone_intermediary
        
        end_formula =  ( installation_or_replacement * equipment_installed *
                        registered_GEMS * gems_cooling_capacity_path * climate_zone_condition )
        
        return end_formula