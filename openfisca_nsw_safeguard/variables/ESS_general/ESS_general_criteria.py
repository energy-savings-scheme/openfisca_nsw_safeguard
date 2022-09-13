from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

class ESS__meets_overall_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet the eligibility criteria defined in Clause 5?'

    def formula(buildings, period, parameters):
        is_not_unlawful_activity = np.logical_not(
            buildings('ESS__is_unlawful_activity', period)
            )

        return(
            is_not_unlawful_activity
            )


class ESS__is_unlawful_activity(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the ESS activity an unlawful activity?'


class ESS__equipment_is_not_resold_reused_or_refurbished(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment removed or replaced as part of an ESS activity, not a. resold, b. reused or c. refurbished?'
    
    def formula(buildings, period, parameters):
        equipment_is_resold = buildings('ESS__equipment_is_resold', period)
        equipment_is_reused = buildings('ESS__equipment_is_reused', period)
        equipment_is_refurbished = buildings('ESS__equipment_is_refurbished', period)

        return np.logical_not(
            equipment_is_resold +
            equipment_is_reused +
            equipment_is_refurbished
        )


class ESS__equipment_is_resold(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Will or has the ACP resold the equipment replaced or removed as part of the activity?'


class ESS__equipment_is_reused(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Will or has the ACP reused the equipment replaced or removed as part of the activity?'


class ESS__equipment_is_refurbished(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Will or has the ACP refurbished the equipment replaced or removed as part of the activity?'
