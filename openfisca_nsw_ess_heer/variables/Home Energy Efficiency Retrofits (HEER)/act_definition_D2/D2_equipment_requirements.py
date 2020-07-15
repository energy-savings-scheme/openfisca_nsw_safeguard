# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

class D2_new_equipment_is_secondary_glazing_product(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new equipment a secondary glazing product?'
    # need to check if the material the product is made is a condition - i.e. does it matter


class D2_new_equipment_is_fitted_to_existing_single_glazed_window(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new equipment fitted to an existing single glazed window?'


class D2_new_product_forms_still_air_gap(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new equipment form a still air gap?'


class new_product_is_secondary_glazing_which_creates_still_air_gap(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new product a secondary glazing product, fitted to an' \
            ' existing window, which creates a still air gap between the' \
            ' existing window and the new glazing?'

    def formula(buildings, period, parameters):
        is_secondary_glazing = buildings('D2_new_equipment_is_secondary_glazing_product', period)
        fitted_to_existing_window = buildings('D2_new_equipment_is_fitted_to_existing_single_glazed_window', period)
        forms_still_air_gap = buildings('D2_new_product_forms_still_air_gap', period)
        return is_secondary_glazing * fitted_to_existing_window * forms_still_air_gap


class NewProductWERSCoolingStarRating(Enum):
    one_star = u'Equipment has a WERS Cooling Star Rating of 1 star, following installation of glazing'
    one_and_a_half_stars = u'Equipment has a WERS Cooling Star Rating of 1.5 stars, following installation of glazing'
    two_stars = u'Equipment has a WERS Cooling Star Rating of 2 stars, following installation of glazing'
    two_and_a_half_stars = u'Equipment has a WERS Cooling Star Rating of 2.5 stars, following installation of glazing'
    three_stars = u'Equipment has a WERS Cooling Star Rating of 3 stars, following installation of glazing'
    three_and_a_half_stars = u'Equipment has a WERS Cooling Star Rating of 3.5 stars, following installation of glazing'
    four_stars = u'Equipment has a WERS Cooling Star Rating of 4 stars, following installation of glazing'
    four_and_a_half_stars = u'Equipment has a WERS Cooling Star Rating of 4.5 stars, following installation of glazing'
    five_stars = u'Equipment has a WERS Cooling Star Rating of 5 stars, following installation of glazing'
    five_and_a_half_stars = u'Equipment has a WERS Cooling Star Rating of 5.5 stars, following installation of glazing'
    six_stars = u'Equipment has a WERS Cooling Star Rating of 6 stars, following installation of glazing'
    seven_stars = u'Equipment has a WERS Cooling Star Rating of 7 stars, following installation of glazing'
    eight_stars = u'Equipment has a WERS Cooling Star Rating of 8 stars, following installation of glazing'
    nine_stars = u'Equipment has a WERS Cooling Star Rating of 9 stars, following installation of glazing'
    ten_stars = u'Equipment has a WERS Cooling Star Rating of 10 stars, following installation of glazing'


class new_product_WERS_cooling_star_rating(Variable):
    value_type = Enum
    entity = Building
    possible_values = NewProductWERSCoolingStarRating
    default_value = NewProductWERSCoolingStarRating.one_star
    definition_period = ETERNITY
    label = "What is the WERS rating in cooling mode, following installation of the new glazing product?"


class NewProductWERSHeatingStarRating(Enum):
    one_star = u'Equipment has a WERS Heating Star Rating of 1 star, following installation of glazing'
    one_and_a_half_stars = u'Equipment has a WERS Heating Star Rating of 1.5 stars, following installation of glazing'
    two_stars = u'Equipment has a WERS Heating Star Rating of 2 stars, following installation of glazing'
    two_and_a_half_stars = u'Equipment has a WERS Heating Star Rating of 2.5 stars, following installation of glazing'
    three_stars = u'Equipment has a WERS Heating Star Rating of 3 stars, following installation of glazing'
    three_and_a_half_stars = u'Equipment has a WERS Heating Star Rating of 3.5 stars, following installation of glazing'
    four_stars = u'Equipment has a WERS Heating Star Rating of 4 stars, following installation of glazing'
    four_and_a_half_stars = u'Equipment has a WERS Heating Star Rating of 4.5 stars, following installation of glazing'
    five_stars = u'Equipment has a WERS Heating Star Rating of 5 stars, following installation of glazing'
    five_and_a_half_stars = u'Equipment has a WERS Heating Star Rating of 5.5 stars, following installation of glazing'
    six_stars = u'Equipment has a WERS Heating Star Rating of 6 stars, following installation of glazing'
    seven_stars = u'Equipment has a WERS Heating Star Rating of 7 stars, following installation of glazing'
    eight_stars = u'Equipment has a WERS Heating Star Rating of 8 stars, following installation of glazing'
    nine_stars = u'Equipment has a WERS Heating Star Rating of 9 stars, following installation of glazing'
    ten_stars = u'Equipment has a WERS Heating Star Rating of 10 stars, following installation of glazing'


class new_product_WERS_heating_star_rating(Variable):
    value_type = Enum
    entity = Building
    possible_values = NewProductWERSHeatingStarRating
    default_value = NewProductWERSHeatingStarRating.one_star
    definition_period = ETERNITY
    label = "What is the WERS rating in heating mode, following installation of the new glazing product?"


class D2_above_minimum_WERS_heating_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the window or door have a minimum six star or higher WERS' \
            ' rating in heating mode?'

    def formula(buildings, period, parameters):
        WERS_heating_star_rating = buildings('new_product_WERS_heating_star_rating', period)
        six_stars = (WERS_heating_star_rating == NewProductWERSHeatingStarRating.six_stars)
        seven_stars = (WERS_heating_star_rating == NewProductWERSHeatingStarRating.seven_stars)
        eight_stars = (WERS_heating_star_rating == NewProductWERSHeatingStarRating.eight_stars)
        nine_stars = (WERS_heating_star_rating == NewProductWERSHeatingStarRating.nine_stars)
        ten_stars = (WERS_heating_star_rating == NewProductWERSHeatingStarRating.ten_stars)
        return six_stars + seven_stars + eight_stars + nine_stars + ten_stars


class D2_window_warranty_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the warranty length of the new window, in years?'


class D2_door_warranty_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the warranty length of the new door, in years?'


class D2_door_or_window_has_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the warranty length of the door or window exceed the minimum' \
            ' warranty length of 5 years?'

    def formula(buildings, period, parameters):
        minimum_warranty_length = 5
        window_warranty_length = buildings('D2_window_warranty_length', period)
        door_warranty_length = buildings('D2_door_warranty_length', period)
        is_secondary_glazing_product = buildings('D2_new_equipment_is_secondary_glazing_product', period)
        return ((window_warranty_length >= minimum_warranty_length)
        + (door_warranty_length >= minimum_warranty_length) * is_secondary_glazing_product)
