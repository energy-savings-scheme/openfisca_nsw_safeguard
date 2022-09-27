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
        

        new_installation *

        #TODO conditional Q: if not a new installation, then replacement and qualified removal
        #replacement *
        #qualified_removal_replacement *

        qualified_install *
        equipment_installed *

        (np.logical_not(not_residential_building)) *

        # TODO Conditional Q: if Residential is true, then Class 2
        # class_2_building *

        registered_GEMS *
        cooling_capacity *

        #TODO Conditional Q: if yes, then TCPSF greater
        #TODO Conditional Q: if no, then AEER greater
        #TCPSF_greater 
        #AEER_greater

        #TODO climate zone input goes here, but not sure how this works in the formula
        #TODO if climate zone is average or hot then
        #TODO if climate zone is cool then 

        #climate_zone 
        



    return is_eligible