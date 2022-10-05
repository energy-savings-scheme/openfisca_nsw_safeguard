from openfisca_core.variables import *
from openfisca_core.periods import YEAR, ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

from datetime import datetime as py_datetime
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
        equipment_not_reused_resold_or_refurbished = buildings(
            'ESS__equipment_is_not_resold_reused_or_refurbished', period)
        appropriate_disposal_after_15_April_2016 = buildings(
            'ESS__appropriate_disposal_of_equipment_after_15_April_2016', period)
        reduces_energy_consumption = buildings(
            'ESS__reduces_energy_consumption', period)
        registered_ACP = buildings(
            'ESS_registered_ACP', period)
        

        return(
            is_not_unlawful_activity *
            equipment_not_reused_resold_or_refurbished *
            appropriate_disposal_after_15_April_2016 *
            reduces_energy_consumption *
            registered_ACP
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
    metadata = {
        'display-question' : 'Is the removed End-User equipment re-sold, refurbished or re-used?'
    }
    
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
    metadata = {
        'display_question' : 'Will your End-User equipment be disposed of in accordance with legal requirements, (including by obtaining evidence for any refrigerants being disposed of or recycled)?'
    }

    def formula(buildings, period, parameters):
        implementation_date = (buildings('ESS__implementation_date', period).astype('datetime64[D]'))
        enforcement_date = np.datetime64('2016-04-15')
        on_or_after_15_April_2016 = (
            implementation_date > enforcement_date)

        activity_occurred_in_Metro = buildings(
            'ESS__activity_occurred_in_Metro_Levy_Area', period)
        lighting_disposed_of_appropriately = buildings(
            'ESS__lighting_mercury_disposed_appropriately', period)
        refrigerant_recycling_evidence_is_available = buildings(
            'ESS__recycling_evidence_for_refrigerants_is_obtained', period)


        return(
            np.logical_not(on_or_after_15_April_2016) +
            (
                on_or_after_15_April_2016 *
                (
                    (   activity_occurred_in_Metro *
                        lighting_disposed_of_appropriately
                    ) +
                    np.logical_not(activity_occurred_in_Metro)
                ) *
                refrigerant_recycling_evidence_is_available
            )
        )


class ESS__activity_occurred_in_Metro_Levy_Area(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Did the activity take place in a Metro Levy Area?'

    def formula(buildings, period, parameters):
        postcode = buildings('ESS__postcode', period)
        metro_levy_areas = parameters(period).ESS.ESS_general.table_A25_metro_levy_area
        return metro_levy_areas.calc(postcode)


class ESS__lighting_mercury_disposed_appropriately(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has any mercury present in removed lighting products been disposed of appropriately?'



class ESS__recycling_evidence_for_refrigerants_is_obtained(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has recycling evidence been obtained for any refrigerants disposed of as part of the activity?'


class ESS__reduces_energy_consumption(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Does the activity reduce energy consumption?'
    metadata = {
        'display_question' : 'Does your activity reduce energy consumption compared to what would have been consumed?'
    }

class ESS_registered_ACP(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Are you an ACP?'
    metadata = {
        'display_question' : 'Are you an ACP?'
    }
    
class ESS_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Did you engage an Accredited Certificate Provider prior to the implementation date?'
    metadata = {
        'display_question' : 'Did you engage an Accredited Certificate Provider prior to the implementation date?',
        'variable-type': 'conditional',
        'dependency': 'ESS_registered_ACP==True'
    }
