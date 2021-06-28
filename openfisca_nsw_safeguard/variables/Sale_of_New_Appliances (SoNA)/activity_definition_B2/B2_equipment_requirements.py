from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

class ESS__SONA_end_user_equipment_is_clothes_dryer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a Clothes Dryer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B2, Equipment Requirement 1.'


class B2_end_user_equipment_is_labelled_for_energy_labelling(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment registered for energy labelling?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B2, Equipment Requirement 2.'


class DryerStarRating(Enum):
    zero_stars = 'Dryer is rated at zero stars.'
    one_star = 'Dryer is rated at one star.'
    one_and_a_half_star = 'Dryer is rated at one and a half star.'
    two_stars = 'Dryer is rated at two stars.'
    two_and_a_half_stars = 'Dryer is rated at two and a half stars.'
    three_stars = 'Dryer is rated at three stars.'
    three_and_a_half_stars = 'Dryer is rated at three and a half stars.'
    four_stars = 'Dryer is rated at four stars.'
    four_and_a_half_stars = 'Dryer is rated at four and a half stars.'
    five_stars = 'Dryer is rated at five stars.'
    five_and_a_half_stars = 'Dryer is rated at five and a half stars.'
    six_stars = 'Dryer is rated at six stars.'
    seven_stars = 'Dryer is rated at seven stars.'
    eight_stars = 'Dryer is rated at eight stars.'
    nine_stars = 'Dryer is rated at nine stars.'
    ten_stars = 'Dryer is rated at ten stars.'

class dryer_star_rating(Variable):
    value_type = Enum
    possible_values = DryerStarRating
    default_value = DryerStarRating.zero_stars
    entity = Building
    definition_period = ETERNITY
    label = 'What is the star rating for the clothes dryer, as' \
            ' rated in GEMS?'


class B2_end_user_equipment_is_not_combination_washer_dryer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment not a combination washer/dryer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 3.'
    #  long term - need to build a "product type" enum and make this "!= combination washer dryer"

    def formula(buildings, period, parameters):
        is_washer_dryer = buildings('B2_end_user_equipment_is_combination_washer_dryer', period)
        return (not(is_washer_dryer))


class B2_end_user_equipment_has_a_load(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment has a load, as recorded in the' \
            ' GEMS Registry?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 4.'

    def formula(buildings, period, parameters):
        equipment_load = buildings('B2_end_user_equipment_load', period)
        condition_has_load = (equipment_load != 0 and equipment_load is not None)
        return condition_has_load


class B2_end_user_equipment_load(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the equipment load of the new end user equipment, in kilograms?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 4.'


class B2_end_user_equipment_is_combination_washer_dryer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a combination washer/dryer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 5.'


class B2_meets_all_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet all of the Equipment' \
            ' Requirements detailed in Activity Definition B1?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1.'

    def formula(buildings, period, parameters):
        is_clothes_dryer = buildings('B2_end_user_equipment_is_clothes_dryer', period)
        is_labelled_for_energy_labelling = buildings('B2_end_user_equipment_is_labelled_for_energy_labelling', period)
        is_not_washer_dryer = buildings('B2_end_user_equipment_is_not_combination_washer_dryer', period)
        has_load = buildings('B2_end_user_equipment_has_a_load', period)
        return (is_clothes_dryer * is_labelled_for_energy_labelling
        * is_not_washer_dryer * has_load)
