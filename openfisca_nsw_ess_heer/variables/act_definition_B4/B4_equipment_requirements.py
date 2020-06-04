# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

class B4_refrigerator_is_in_eligible_group(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment in Refrigerator Group 1, 2 or 3?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B4, Equipment Requirement 1.'

    def formula(buildings, period, parameters):
        refrigerator_group = buildings('refrigerator_or_freezer_group', period)
        RefrigeratorGroup = refrigerator_group.possible_values  # imports functionality of refrigerator group enum from user_inputs
        in_group_1 = (refrigerator_group == RefrigeratorGroup.group_1)
        in_group_2 = (refrigerator_group == RefrigeratorGroup.group_2)
        in_group_3 = (refrigerator_group == RefrigeratorGroup.group_3)
        return in_group_1 + in_group_2 + in_group_3


class B4_refrigerator_has_one_door(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment have one door?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B4, Equipment Requirement 1.'

    def formula(buildings, period, parameters):
        number_of_refrigerator_doors = buildings('number_of_refrigerator_doors', period)
        return (number_of_refrigerator_doors == 1)


class B4_refrigerator_in_eligible_group_with_one_door(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment in Refrigerator Group 1, 2, or 3, ' \
            ' and does it have one door?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B4, Equipment Requirement 1.'

    def formula(buildings, period, parameters):
        in_eligible_group = buildings('B4_refrigerator_is_in_eligible_group', period)
        has_one_door = buildings('B4_refrigerator_has_one_door', period)
        return in_eligible_group * has_one_door


class B4_end_user_equipment_is_labelled_for_energy_labelling(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment registered for energy labelling?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 2.'


class B4_end_user_equipment_has_registered_volume(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment have a total volume,' \
            ' recorded in the GEMS Registry?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        refrigerator_volume = buildings('refrigerator_or_freezer_capacity', period)
        condition_has_volume = (refrigerator_volume != 0 and refrigerator_volume != None)
        return condition_has_volume


class B4_meets_all_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet all of the Equipment' \
            ' Requirements detailed in Activity Definition B1?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1.'

    def formula(buildings, period, parameters):
        in_eligible_group_and_has_one_door = buildings('B4_refrigerator_in_eligible_group_with_one_door', period)
        is_labelled_for_energy_labelling = buildings('B4_end_user_equipment_is_labelled_for_energy_labelling', period)
        has_volume = buildings('B4_end_user_equipment_has_registered_volume', period)
        return (is_dishwasher * is_labelled_for_energy_labelling * has_volume)
