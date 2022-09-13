from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np
from datetime import date

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


class ESS__implementation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the implementation date for the Activity?'
    # TO DO - pull in implementation dates from method specific implementation dates using
    # method enum


class ESS__appropriate_disposal_of_equipment_after_15_April_2016(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the removed or replaced equipment been disposed of appropriately, in accordance' \
            ' requirements put in place from 15 April 2016?'

    def formula(buildings, period, parameters):
        implementation_date = buildings('ESS__implementation_date', period)
        on_or_after_15_April_2016 = (
            implementation_date >= 2016-4-15
        ) # note datetime formatting here




class ESS__activity_occurred_in_Metro_Levy_Area(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Did the activity take place in a Metro Levy Area?'

    def formula(buildings, period, parameters):
        postcode = buildings('ESS__postcode', period)
        metro_levy_areas = parameters(period).ESS.ESS_general.table_A25_metro_levy_area
        in_metro_levy_area = metro_levy_areas.calc(postcode)
        return in_metro_levy_area 


class ESS__lighting_mercury_disposed_appropriately_in_Metro_Levy_Area(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has any mercury present in removed lighting products been disposed of appropriately, in a Metro Levy Area?'






class ESS__lighting_mercury_disposed_appropriately(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has any mercury present in removed lighting products been disposed of appropriately?'
