from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

class PDRS__HVAC2_new_install(Variable):
    """ The variables for the new equipment install path on the HVAC2 eligibility page
        This is the base default path of HVAC2 Eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the requirements of the HVAC2 Activity?'
    metadata = {
        "alias": "HVAC2 new equipment install is an eligible activity"
    }


    def formula(buildings, period, parameters):
        new_installation = buildings('PDRS_HVAC_2_installation', period)
        qualified_install = buildings('Implementation_is_performed_by_qualified_person', period)
        equipment_installed = buildings('Equipment_is_installed', period)
        not_residential_building = buildings('PDRS__residential_building', period)
        registered_GEMS = buildings('HVAC2_appliance_is_registered_in_GEMS', period)
        cooling_capacity = buildings('new_AC_cooling_capacity', period)
        TCPSF_greater = buildings('HVAC_2_TCPSF_greater_than_minimum', period)

        ACClimateZone = climate_zone.possible_values
        climate_zone = buildings('AC_climate_zone', period)
        in_average_zone = (climate_zone == ACClimateZone.average_zone)
        in_cold_zone = (climate_zone == ACClimateZone.cold_zone)
        heating_capacity = buildings('new_AC_heating_capacity', period)
        HSPF_mixed_value = buildings('AC_HSPF_mixed', period)
        ACOP_value = buildings ('AC_ACOP', period)
        HSPF_cooling_value = buildings('AC_HSPF_cold', period)


        meets_base_install_requirements = (
        new_installation *
        qualified_install *
        equipment_installed *
        not_residential_building *
        registered_GEMS *
        cooling_capacity *
        TCPSF_greater *
        climate_zone *
        in_average_zone *
        heating_capacity *
        HSPF_mixed_value
        )

        return meets_base_install_requirements


class PDRS__HVAC2_replacement(Variable):
    """ The variables for the replacement equipment path on the HVAC2 eligibility page
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the requirements of the HVAC2 Activity?'
    metadata = {
        "alias": "HVAC2 equipment replacement is an eligible activity"
    }


    def formula(buildings, period, parameters):
        replacement = buildings('PDRS_HVAC_2_replacement', period)
        qualified_install = buildings('Implementation_is_performed_by_qualified_person', period)
        qualified_removal_replacement = buildings('Equipment_is_removed', period)
    
        meets_replacement_equipment_requirements = (
        replacement *
        qualified_install *
        qualified_removal_replacement
        )

        return meets_replacement_equipment_requirements


class PDRS__HVAC2_residential(Variable):
    """ The variables for the residential equipment path on the HVAC2 eligibility page
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the equipment been installed in a residential building?'
    metadata = {
        "alias": "HVAC2 Is An Eligible Activity"
    }


    def formula(buildings, period, parameters):
        not_residential_building = buildings('PDRS__residential_building', period)
        class_2_building = buildings('is_installed_centralised_system_common_area_BCA_Class2_building', period)

        meets_residential_install_requirements = (
        np.logical_not(not_residential_building + class_2_building)
        )
        
        return meets_residential_install_requirements
        

class PDRS__HVAC2_no_GEMS_cooling_capacity(Variable):
    """ The variables for no cooling capacity on GEMS path on the HVAC2 eligibility page
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment have a cooling capacity on GEMS?'
    metadata = {
        "alias": "No cooling capacity on GEMS"
    }

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('new_AC_cooling_capacity', period)
        AEER_greater = buildings('HVAC_2_AEER_greater_than_minimum', period)

        meets_cooling_capacity_requirements = (
        np.logical_not(cooling_capacity) + AEER_greater
        )

        return meets_cooling_capacity_requirements


class PDRS__HVAC2_heating_capacity_hot_zone(Variable):
    """ The variables for heating capacity in a hot zone ];path on the HVAC2 eligibility page
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment have a heating capacity on GEMS?'
    metadata = {
        "alias": "No heating capacity in a hot zone on GEMS"
    }

    def formula(buildings, period, parameters):
        ACClimateZone = climate_zone.possible_values
        climate_zone = buildings('AC_climate_zone', period)
        in_hot_zone = (climate_zone == ACClimateZone.hot_zone)
        heating_capacity = buildings('new_AC_heating_capacity', period)
        HSPF_mixed_value = buildings('AC_HSPF_mixed', period)
        ACOP_value = buildings ('AC_ACOP', period)

        if in_hot_zone is True and heating_capacity:
        meets_heating_capacity_requirements = HSPF_mixed_value   

        elif in_hot_zone is True and heating_capacity is False:
        meets_heating_capacity_requirements = ACOP_value
       

class PDRS__HVAC2_heating_capacity_cold_zone(Variable):
    """ The variables for heating capacity in a cold zone path on the HVAC2 eligibility page
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment have a heating capacity on GEMS?'
    metadata = {
        "alias": "No heating capacity in a hot zone on GEMS"
    }

    def formula(buildings, period, parameters):
        ACClimateZone = climate_zone.possible_values
        climate_zone = buildings('AC_climate_zone', period)
        in_hot_zone = (climate_zone == ACClimateZone.hot_zone)
        heating_capacity = buildings('new_AC_heating_capacity', period)
        HSPF_mixed_value = buildings('AC_HSPF_mixed', period)
        ACOP_value = buildings ('AC_ACOP', period)

        if in_hot_zone is True and heating_capacity:
        meets_heating_capacity_requirements = HSPF_mixed_value   

        elif in_hot_zone is True and heating_capacity is False:
        meets_heating_capacity_requirements = ACOP_value
    

        is_eligible = (
          
        )


        return is_eligible


        has to meet 
        new_installation or replacement
        qualified_install
        equipment_installed or qualified_removal_replacement

        not_residential_building or np.logical_not(not_residential_building)
                                    class_2_building

        registered_GEMS
        
        cooling_capacity or np.logical_not(cooling_capacity)
        TCPSF_greater or AEER_greater

        climate_zone 

        in_average_zone or in_hot_zone or in_cold_zone
        heating_capacity or np.logical_not(heating_capacity)
        HSPF_mixed_value or ACOP_value