from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_SONA_television_equipment_is_television(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a Television?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B5, Equipment Requirement 1.'


class ESS_SONA_television_end_user_equipment_is_labelled_for_energy_labelling(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment registered for energy labelling?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 2.'


class TelevisionStarRating(Enum):
    zero_stars = 'Television is rated at zero stars.'
    one_star = 'Television is rated at one star.'
    one_and_a_half_star = 'Television is rated at one and a half star.'
    two_stars = 'Television is rated at two stars.'
    two_and_a_half_stars = 'Television is rated at two and a half stars.'
    three_stars = 'Television is rated at three stars.'
    three_and_a_half_stars = 'Television is rated at three and a half stars.'
    four_stars = 'Television is rated at four stars.'
    four_and_a_half_stars = 'Television is rated at four and a half stars.'
    five_stars = 'Television is rated at five stars.'
    five_and_a_half_stars = 'Television is rated at five and a half stars.'
    six_stars = 'Television is rated at six stars.'
    seven_stars = 'Television is rated at seven stars.'
    eight_stars = 'Television is rated at eight stars.'
    nine_stars = 'Television is rated at nine stars.'
    ten_stars = 'Television is rated at ten stars.'

class television_star_rating(Variable):
    value_type = Enum
    possible_values = TelevisionStarRating
    default_value = TelevisionStarRating.zero_stars
    entity = Building
    definition_period = ETERNITY
    label = 'What is the star rating for the television, as' \
            ' rated in GEMS?'
    # for use in Activity Definition B3.


class television_screen_size(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the screen size for the television, as' \
            ' rated in GEMS?'


class ESS_SONA_television_end_user_equipment_has_registered_screen_size(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment have a registered screen size,' \
            ' recorded in the GEMS Registry?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        screen_size = buildings('television_screen_size', period)
        condition_screen_size_is_not_zero = ((screen_size != 0)
        and (screen_size != 0.0) and (screen_size is not None))
        return condition_screen_size_is_not_zero


class ESS_SONA_television_meets_all_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet all of the Equipment' \
            ' Requirements detailed in Activity Definition B1?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1.'

    def formula(buildings, period, parameters):
        is_television = buildings('ESS_SONA_television_equipment_is_television', period)
        is_labelled_for_energy_labelling = buildings('ESS_SONA_television_end_user_equipment_is_labelled_for_energy_labelling', period)
        has_screen_size = buildings('ESS_SONA_television_end_user_equipment_has_registered_screen_size', period)
        return (is_television * is_labelled_for_energy_labelling * has_screen_size)
