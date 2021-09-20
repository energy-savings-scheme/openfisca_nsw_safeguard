from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_SONA_1_door_refrigerator_refrigerator_is_in_eligible_group(Variable):
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


class ESS_SONA_1_door_refrigerator_refrigerator_has_one_door(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment have one door?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition ESS_SONA_1_door_refrigerator, Equipment Requirement 1.'

    def formula(buildings, period, parameters):
        number_of_refrigerator_doors = buildings('number_of_refrigerator_doors', period)
        return (number_of_refrigerator_doors == 1)


class ESS_SONA_1_door_refrigerator_refrigerator_in_eligible_group_with_one_door(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment in Refrigerator Group 1, 2, or 3, ' \
            ' and does it have one door?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition ESS_SONA_1_door_refrigerator, Equipment Requirement 1.'

    def formula(buildings, period, parameters):
        in_eligible_group = buildings('ESS_SONA_1_door_refrigerator_refrigerator_is_in_eligible_group', period)
        has_one_door = buildings('ESS_SONA_1_door_refrigerator_refrigerator_has_one_door', period)
        return in_eligible_group * has_one_door


class ESS_SONA_1_door_refrigerator_end_user_equipment_is_labelled_for_energy_labelling(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment registered for energy labelling?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 2.'


class RefrigeratorStarRating(Enum):
    zero_stars = 'Refrigerator is rated at zero stars.'
    one_star = 'Refrigerator is rated at one star.'
    one_and_a_half_star = 'Refrigerator is rated at one and a half star.'
    two_stars = 'Refrigerator is rated at two stars.'
    two_and_a_half_stars = 'Refrigerator is rated at two and a half stars.'
    three_stars = 'Refrigerator is rated at three stars.'
    three_and_a_half_stars = 'Refrigerator is rated at three and a half stars.'
    four_stars = 'Refrigerator is rated at four stars.'
    four_and_a_half_stars = 'Refrigerator is rated at four and a half stars.'
    five_stars = 'Refrigerator is rated at five stars.'
    five_and_a_half_stars = 'Refrigerator is rated at five and a half stars.'
    six_stars = 'Refrigerator is rated at six stars.'
    seven_stars = 'Refrigerator is rated at seven stars.'
    eight_stars = 'Refrigerator is rated at eight stars.'
    nine_stars = 'Refrigerator is rated at nine stars.'
    ten_stars = 'Refrigerator is rated at ten stars.'

class refrigerator_star_rating(Variable):
    value_type = Enum
    possible_values = RefrigeratorStarRating
    default_value = RefrigeratorStarRating.zero_stars
    entity = Building
    definition_period = ETERNITY
    label = 'What is the star rating for the dishwasher, as' \
            ' rated in GEMS?'
    # for use in Activity Definition B3.


class ESS_SONA_1_door_refrigerator_end_user_equipment_has_registered_volume(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment have a total volume,' \
            ' recorded in the GEMS Registry?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        refrigerator_volume = buildings('refrigerator_or_freezer_capacity', period)
        condition_volume_is_not_zero = ((refrigerator_volume != 0) and (refrigerator_volume != 0.0)
        and (refrigerator_volume is not None))
        return condition_volume_is_not_zero


class ESS_SONA_1_door_refrigerator_meets_all_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet all of the Equipment' \
            ' Requirements detailed in Activity Definition B1?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1.'

    def formula(buildings, period, parameters):
        in_eligible_group_and_has_one_door = buildings('ESS_SONA_1_door_refrigerator_refrigerator_in_eligible_group_with_one_door', period)
        is_labelled_for_energy_labelling = buildings('ESS_SONA_1_door_refrigerator_end_user_equipment_is_labelled_for_energy_labelling', period)
        has_volume = buildings('ESS_SONA_1_door_refrigerator_end_user_equipment_has_registered_volume', period)
        return (in_eligible_group_and_has_one_door * is_labelled_for_energy_labelling * has_volume)
