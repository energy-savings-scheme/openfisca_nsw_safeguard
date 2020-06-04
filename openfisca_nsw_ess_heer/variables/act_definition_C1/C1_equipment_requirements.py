# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

class C1_implementation_must_be_residential(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the site where the End User Equipment is located a' \
            ' Residential Site?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1, Equipment Requirement 1.'

    def formula(buildings, period, parameters):
        building_type = buildings('building_type', period)
        BuildingType = building_type.possible_values
        is_residential = (building_type == BuildingType.residential_building)
        return is_residential


class C1_end_user_equipment_is_eligible_group(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment a Refrigerator or Freezer or a' \
            ' combination of the two, classified as Group 1, 2, 3, 4, 5T, 5B,' \
            ' 5S, 6C, 6U or 7, according to AS/NZS 4474.1 or 4474.2?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1, Equipment Requirement 2.'
    #  need to pull equipment groups from AS4474.1 or AS4474.2

    def formula(buildings, period, parameters):
        refrigerator_group = buildings('refrigerator_or_freezer_group', period)
        RefrigeratorGroup = refrigerator_group.possible_values  # imports functionality of refrigerator group enum from user_inputs
        in_group_1 = (refrigerator_group == RefrigeratorGroup.group_1)
        in_group_2 = (refrigerator_group == RefrigeratorGroup.group_2)
        in_group_3 = (refrigerator_group == RefrigeratorGroup.group_3)
        in_group_4 = (refrigerator_group == RefrigeratorGroup.group_4)
        in_group_5B = (refrigerator_group == RefrigeratorGroup.group_5B)
        in_group_5S = (refrigerator_group == RefrigeratorGroup.group_5S)
        in_group_5T = (refrigerator_group == RefrigeratorGroup.group_5T)
        in_group_6C = (refrigerator_group == RefrigeratorGroup.group_6C)
        in_group_6U = (refrigerator_group == RefrigeratorGroup.group_6U)
        in_group_7 = (refrigerator_group == RefrigeratorGroup.group_7)
        return (in_group_1 + in_group_2 + in_group_3 + in_group_4 + in_group_5B
                + in_group_5S + in_group_5T + in_group_6C + in_group_6U + in_group_7)


class refrigerator_or_freezer_is_minimum_capacity(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the capacity of the refrigerator or freezer 200L or more?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1, Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        capacity = buildings('refrigerator_or_freezer_capacity', period)
        condition_minimum_capacity = capacity >= 200
        return condition_minimum_capacity


class refrigerator_or_freezer_is_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing refrigerator or freezer in working order?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1, Equipment Requirement 4.'


class another_fridge_available_to_provide_primary_refrigeration(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is there another Refrigerator or Freezer available to provide' \
            ' primary refrigeration or freezer services?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1, Equipment Requirement 5.'


class one_fewer_fridge_following_activity(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is there 1 fewer fridge at the Site following the implementation activity?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1, Equipment Requirement 6.'


class C1_requirements_are_met(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Have all of the requirements required to conduct Activity' \
            ' Definition C1 been met?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1.'

    def formula(buildings, period, parameters):
        is_residential = buildings('C1_implementation_must_be_residential', period)
        existing_fridge_in_eligible_group = buildings('C1_end_user_equipment_is_eligible_group', period)
        refrigerator_or_freezer_is_minimum_capacity = buildings('refrigerator_or_freezer_is_minimum_capacity', period)
        existing_fridge_in_working_order = buildings('refrigerator_or_freezer_is_in_working_order', period)
        primary_fridge_available = buildings('another_fridge_available_to_provide_primary_refrigeration', period)
        one_fewer_fridge = buildings('one_fewer_fridge_following_activity', period)
        return (is_residential * existing_fridge_in_eligible_group * refrigerator_or_freezer_is_minimum_capacity
        * existing_fridge_in_working_order * primary_fridge_available * one_fewer_fridge)
