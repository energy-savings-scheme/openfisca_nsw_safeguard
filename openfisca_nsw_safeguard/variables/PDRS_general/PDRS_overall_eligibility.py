from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

class PDRS__is_eligible_activity(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the overarching requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible Activity",
    }

    def formula(buildings, period, parameters):
        provides_capacity_to_reduce_demand = buildings('PDRS__provides_capacity_to_reduce_demand', period)
        is_eligible_for_PDRS_creation = buildings('PDRS__is_eligible_for_PDRS_creation', period)
        is_in_PDRS_jurisdiction = buildings('PDRS__is_in_PDRS_jurisdiction', period)
        is_unlawful_activity = buildings('PDRS__is_unlawful_activity', period)
        greenhouse_emissions_increase = buildings('PDRS__greenhouse_emissions_increase', period)
        activity_meets_mandatory_requirement = buildings('PDRS__meets_mandatory_requirement', period)
        is_standard_control_service = buildings('PDRS__is_standard_control_service', period)
        is_prescribed_transmission_service = buildings('PDRS__is_prescribed_transmission_service', period)
        is_non_network_option = buildings('PDRS__is_non_network_option', period)
        reduces_safety_levels = buildings('PDRS__reduces_safety_levels', period)

        is_eligible_peak_demand_reduction_activity = (
        provides_capacity_to_reduce_demand * 
        is_eligible_for_PDRS_creation *
        is_in_PDRS_jurisdiction *
        (np.logical_not(is_unlawful_activity))        
        )

        is_not_eligible_peak_demand_reduction_activity = (
        (greenhouse_emissions_increase) +
        (activity_meets_mandatory_requirement)
        +
        (is_standard_control_service
        + is_prescribed_transmission_service
        * (np.logical_not(is_non_network_option))
        )
        + reduces_safety_levels
        )

        is_eligible = (
          is_eligible_peak_demand_reduction_activity *
          (np.logical_not(is_not_eligible_peak_demand_reduction_activity))
        )
        return is_eligible


class PDRS__provides_capacity_to_reduce_demand(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the overarching requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible Activity",
    }


class PDRS__is_eligible_for_PDRS_creation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the overarching requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible Activity",
    }


class PDRS__is_in_PDRS_jurisdiction(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the overarching requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible Activity",
    }


class PDRS__is_unlawful_activity(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the overarching requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible Activity",
    }


class PDRS__greenhouse_emissions_increase(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the overarching requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible Activity",
    }


class PDRS__meets_mandatory_requirement(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the overarching requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible Activity",
    }


class PDRS__is_standard_control_service(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the overarching requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible Activity",
    }


class PDRS__is_prescribed_transmission_service(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the overarching requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible Activity",
    }


class PDRS__is_non_network_option(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the overarching requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible Activity",
    }


class PDRS__reduces_safety_levels(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible within the overarching requirements of the PDRS?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Is Eligible Activity",
    }
