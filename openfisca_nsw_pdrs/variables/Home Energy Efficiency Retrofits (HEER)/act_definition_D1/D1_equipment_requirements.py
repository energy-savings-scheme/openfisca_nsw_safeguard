# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class new_end_user_equipment_is_WERS_rated_window(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the New End-User Equipment a window product, glazing and frame' \
            ' that is rated by WERS?'


class new_end_user_equipment_is_WERS_rated_door(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the New End-User Equipment a door product, glazing and frame' \
            ' that is rated by WERS?'


class new_end_user_equipment_is_WERS_rated_window_or_door(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the New End-User Equipment a window or door product, including' \
            ' both glazing and frame, that is rated by WERS?'

    def formula(buildings, period, parameters):
        WERS_rated_window = buildings('new_end_user_equipment_is_WERS_rated_window', period)
        WERS_rated_door = buildings('new_end_user_equipment_is_WERS_rated_door', period)
        return WERS_rated_window + WERS_rated_door


class new_end_user_equipment_is_single_glazed_insulating_glass_unit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the New End-User Equipment a single glazed insulating glass unit?'


class new_end_user_equipment_is_double_glazed_insulating_glass_unit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the New End-User Equipment a double glazed insulating glass unit?'


class new_end_user_equipment_is_triple_glazed_insulating_glass_unit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the New End-User Equipment a triple glazed insulating glass unit?'


class new_end_user_equipment_is_single_double_or_triple_glazed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the New End-User Equipment a single glazed, double glazed or' \
            ' triple glazed insulating glass unit?'

    def formula(buildings, period, parameters):
        is_single_glazed = buildings('new_end_user_equipment_is_single_glazed_insulating_glass_unit', period)
        is_double_glazed = buildings('new_end_user_equipment_is_double_glazed_insulating_glass_unit', period)
        is_triple_glazed = buildings('new_end_user_equipment_is_triple_glazed_insulating_glass_unit', period)
        return is_single_glazed + is_double_glazed + is_triple_glazed


class complies_with_AS_2047_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End-User Equipment comply with AS 2047?'
    # note we probably need to figure out exactly WHICH requirements

class complies_with_AS_1288_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End-User Equipment comply with AS 1288?'
    # note we probably need to figure out exactly WHICH requirements


class complies_with_AS_2047_and_AS_1288(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End-User Equipment comply with AS 2047 and AS 1288?'

    def formula(buildings, period, parameters):
        complies_with_AS_2047 = buildings('complies_with_AS_2047', period)
        complies_with_AS_1288 = buildings('complies_with_AS_1288', period)
        return complies_with_AS_2047 * complies_with_AS_1288


class WERSHeatingStarRating(Enum):
    one_star = u'Equipment has a WERS Heating Star Rating of 1 star'
    one_and_a_half_stars = u'Equipment has a WERS Heating Star Rating of 1.5 stars'
    two_stars = u'Equipment has a WERS Heating Star Rating of 2 stars'
    two_and_a_half_stars = u'Equipment has a WERS Heating Star Rating of 2.5 stars'
    three_stars = u'Equipment has a WERS Heating Star Rating of 3 stars'
    three_and_a_half_stars = u'Equipment has a WERS Heating Star Rating of 3.5 stars'
    four_stars = u'Equipment has a WERS Heating Star Rating of 4 stars'
    four_and_a_half_stars = u'Equipment has a WERS Heating Star Rating of 4.5 stars'
    five_stars = u'Equipment has a WERS Heating Star Rating of 5 stars'
    five_and_a_half_stars = u'Equipment has a WERS Heating Star Rating of 5.5 stars'
    six_stars = u'Equipment has a WERS Heating Star Rating of 6 stars'
    seven_stars = u'Equipment has a WERS Heating Star Rating of 7 stars'
    eight_stars = u'Equipment has a WERS Heating Star Rating of 8 stars'
    nine_stars = u'Equipment has a WERS Heating Star Rating of 9 stars'
    ten_stars = u'Equipment has a WERS Heating Star Rating of 10 stars'
    #  need to check if these are the appropriate divisions for HERS Star Ratings


class WERS_heating_star_rating(Variable):
    value_type = Enum
    entity = Building
    possible_values = WERSHeatingStarRating
    default_value = WERSHeatingStarRating.one_star
    definition_period = ETERNITY
    label = "What is the WERS rating in heating mode?"


class WERSCoolingStarRating(Enum):
    one_star = u'Equipment has a WERS Cooling Star Rating of 1 star'
    one_and_a_half_stars = u'Equipment has a WERS Cooling Star Rating of 1.5 stars'
    two_stars = u'Equipment has a WERS Cooling Star Rating of 2 stars'
    two_and_a_half_stars = u'Equipment has a WERS Cooling Star Rating of 2.5 stars'
    three_stars = u'Equipment has a WERS Cooling Star Rating of 3 stars'
    three_and_a_half_stars = u'Equipment has a WERS Cooling Star Rating of 3.5 stars'
    four_stars = u'Equipment has a WERS Cooling Star Rating of 4 stars'
    four_and_a_half_stars = u'Equipment has a WERS Cooling Star Rating of 4.5 stars'
    five_stars = u'Equipment has a WERS Cooling Star Rating of 5 stars'
    five_and_a_half_stars = u'Equipment has a WERS Cooling Star Rating of 5.5 stars'
    six_stars = u'Equipment has a WERS Cooling Star Rating of 6 stars'
    seven_stars = u'Equipment has a WERS Cooling Star Rating of 7 stars'
    eight_stars = u'Equipment has a WERS Cooling Star Rating of 8 stars'
    nine_stars = u'Equipment has a WERS Cooling Star Rating of 9 stars'
    ten_stars = u'Equipment has a WERS Cooling Star Rating of 10 stars'
    #  need to check if these are the appropriate divisions for HERS Star Ratings


class WERS_cooling_star_rating(Variable):
    value_type = Enum
    entity = Building
    possible_values = WERSCoolingStarRating
    default_value = WERSCoolingStarRating.one_star
    definition_period = ETERNITY
    label = "What is the WERS rating in cooling mode?"


class above_minimum_WERS_heating_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the window or door have a minimum six star or higher WERS' \
            ' rating in heating mode?'

    def formula(buildings, period, parameters):
        WERS_heating_star_rating = buildings('WERS_heating_star_rating', period)
        six_stars = (WERS_heating_star_rating == WERSHeatingStarRating.six_stars)
        seven_stars = (WERS_heating_star_rating == WERSHeatingStarRating.seven_stars)
        eight_stars = (WERS_heating_star_rating == WERSHeatingStarRating.eight_stars)
        nine_stars = (WERS_heating_star_rating == WERSHeatingStarRating.nine_stars)
        ten_stars = (WERS_heating_star_rating == WERSHeatingStarRating.ten_stars)
        return six_stars + seven_stars + eight_stars + nine_stars + ten_stars


class D1_window_warranty_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the warranty length of the new window, in years?'


class D1_door_warranty_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the warranty length of the new door, in years?'


class door_or_window_has_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the warranty length of the door or window exceed the minimum' \
            ' warranty length of 5 years?'

    def formula(buildings, period, parameters):
        minimum_warranty_length = 5
        window_warranty_length = buildings('D1_window_warranty_length', period)
        door_warranty_length = buildings('D1_door_warranty_length', period)
        new_end_user_equipment_is_WERS_rated_window = buildings('new_end_user_equipment_is_WERS_rated_window', period)
        new_end_user_equipment_is_WERS_rated_door = buildings('new_end_user_equipment_is_WERS_rated_door', period)
        return (((window_warranty_length >= minimum_warranty_length) * new_end_user_equipment_is_WERS_rated_window)
        + ((door_warranty_length >= minimum_warranty_length) * new_end_user_equipment_is_WERS_rated_door))


class D1_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the implementation for Activity Definition D1 meet all of' \
            ' equipment requirements?'

    def formula(buildings, period, parameters):
        is_rated_window_or_door = buildings('new_end_user_equipment_is_WERS_rated_window_or_door', period)
        is_glazed = buildings('new_end_user_equipment_is_single_double_or_triple_glazed', period)
        complies_with_relevant_standards = buildings('complies_with_AS_2047_and_AS_1288', period)
        above_minimum_WERS_heating_rating = buildings('above_minimum_WERS_heating_rating', period)
        has_minimum_warranty_length = buildings('door_or_window_has_minimum_warranty_length', period)
        return (is_rated_window_or_door * is_glazed * complies_with_relevant_standards
        * above_minimum_WERS_heating_rating * has_minimum_warranty_length)
