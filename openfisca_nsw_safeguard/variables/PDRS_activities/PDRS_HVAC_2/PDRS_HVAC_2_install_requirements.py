import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

## detailed in PDRS activity XX

class PDRS_HVAC_2_install_meets_eligibility_requirements(Variable):
    """ ESS_PDRS_is_residential is found in appliances_eligibility_requirements
    """
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Eligibility' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC install meets eligibility requirements",
        "regulation_reference": PDRS_2022["HEAB", "AC_install", "eligibility"]
    }

    def formula(buildings, period, parameters):
        is_residential = buildings(
            'ESS_PDRS_is_residential', period)
        no_existing_AC = buildings('No_Existing_AC', period)
        """return np.logical_not(is_residential) * no_existing_AC
        """
        return np.logical_not(is_residential) * no_existing_AC


class PDRS_HVAC_2_install_meets_equipment_requirements(Variable):
    """ HVAC2_appliance_is_registered_in_GEMS is found in appliances_equipment_requirements
    """
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the equipment meet all of the Equipment' \
            'Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC Install meets equipment requirements",
        "regulation_reference": PDRS_2022["HEAB", "AC_install", "equipment"]
    }

    def formula(buildings, period, parameters):
        is_in_GEM = buildings(
            'HVAC2_appliance_is_registered_in_GEMS', period)
        has_warranty = buildings(
            'PDRS_HVAC_2_TCSPF_or_AEER_exceeds_benchmark', period)
        demand_response = buildings(
            'Appliance_demand_response_capability', period)

        return is_in_GEM * has_warranty * demand_response


class PDRS_HVAC_2_install_meets_implementation_requirements(Variable):
    """ Equipment_is_installed is found in appliances_implementation_requirements
        Implementation_is_performed_by_qualified_person is found in appliances_implementation_requirements
    """ 
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Implementation' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC Install meets implementation requirements",
        "regulation_reference": PDRS_2022["HEAB", "AC_install", "implementation"]       
    }

    def formula(buildings, period, parameters):
        is_installed = buildings(
            'Equipment_is_installed', period)
        performed_by_qualified_person = buildings(
            'Implementation_is_performed_by_qualified_person', period)
        
        return is_installed * performed_by_qualified_person


class PDRS_HVAC_2_install_meets_all_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC install meets all requirements",
    }

    def formula(buildings, period):
        eligibility = buildings(
            'PDRS_HVAC_2_install_meets_eligibility_requirements', period)
        equipment = buildings(
            'PDRS_HVAC_2_install_meets_equipment_requirements', period)
        implementation = buildings(
            'PDRS_HVAC_2_install_meets_implementation_requirements', period)

        return implementation * eligibility * equipment
