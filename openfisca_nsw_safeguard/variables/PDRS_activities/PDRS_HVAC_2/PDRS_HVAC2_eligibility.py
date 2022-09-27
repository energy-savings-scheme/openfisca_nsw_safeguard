from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

class PDRS__HVAC2_is_eligible_activity(Variable):
    """ This is the formula that pulls in the variables for the HVAC2 eligibility check page
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the requirements of the HVAC2 Activity?'
    metadata = {
        "alias": "HVAC2 Is An Eligible Activity"
    }

    def formula(buildings, period, parameters):
        new_installation = buildings('PDRS_HVAC_2_installation', period)
        replacement = buildings('PDRS_HVAC_2_installation', period)
        qualified_install = buildings('implementation_is_performed_by_qualified_person', period)
        qualified_removal_replacement = buildings('Equipment_is_removed', period)
        equipment_installed = buildings('Equipment_is_installed', period)
        not_residential_building = buildings('PDRS__residential_building', period)
        class_2_building = buildings('is_installed_centralised_system_common_area_BCA_Class2_building', period)
        registered_GEMS = buildings('HVAC2_appliance_is_registered_in_GEMS', period)
        cooling_capacity = buildings('new_AC_cooling_capacity', period)
        AEER_greater = buildings('HVAC_2_AEER_greater_than_minimum', period)
        TCPSF_greater = buildings('HVAC_2_TCPSF_greater_than_minimum', period)
        climate_zone = buildings('AC_climate_zone', period)
        heating_capacity = buildings('new_AC_heating_capacity', period)
        HSPF_mixed_value = buildings('AC_HSPF_mixed', period)
        ACOP_value = buildings ('AC_ACOP', period)
        HSPF_cooling_value = buildings('AC_HSPF_cold', period)

        
        if new_installation is False: 
            conditional_path_replacement = np.logical_not(new_installation) * replacement * qualified_removal_replacement
        else: 
            conditional_path_replacement = new_installation 


        if not_residential_building is False:
            conditional_path_residential = np.logical_not(not_residential_building) * class_2_building
        else:
            conditional_path_residential = not_residential_building


        if cooling_capacity is False:
            conditional_path_cooling = np.logical_not(cooling_capacity) * AEER_greater
        else: 
            conditional_path_cooling = cooling_capacity * TCPSF_greater


        # if climate zone is hot or average and there is a GEMS heating capacity then HSPF
        if climate_zone == in_average_zone or in_hot_zone * heating_capacity:
           conditional_path_HSPF_heating = HSPF_mixed_value
        else:
           #Alisha - this is my attempt to say if climate zone is hot or average and there is no GEMS heating capcity then ACOP value
           #but I may need and elseif climate_zone = in_average_zone or in_hot_zone * np.logical_not(heating-capacity): ?
           conditional_path_HSPF_heating = ACOP_value


        if climate_zone == in_cold_zone:
            conditional_path_HSPF_cooling = HSPF_cooling_value
        else:
            conditional_path_HSPF_cooling = ACOP_value
            

        climate_zone = buildings('AC_climate_zone', period)
        ACClimateZone = climate_zone.possible_values
        in_hot_zone = (climate_zone == ACClimateZone.hot_zone)
        in_average_zone = (climate_zone == ACClimateZone.average_zone)
        in_cold_zone = (climate_zone == ACClimateZone.cold_zone)

        return(
        qualified_install *
        equipment_installed *
        registered_GEMS *
        climate_zone *
        conditional_path_replacement * 
        conditional_path_residential *
        conditional_path_cooling *
        conditional_path_HSPF_heating *
        conditional_path_HSPF_cooling
        )