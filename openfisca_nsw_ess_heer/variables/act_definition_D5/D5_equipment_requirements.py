# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class new_end_user_equipment_is_eligible_type(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a LED Lamp only - ELV, an' \
            ' LED Lamp and Driver, an LED Luminaire-recessed or an LED Lamp' \
            ' only - 240V Self Ballasted, as required in Equipment Requirement' \
            ' 1 in Activity Definition E1, and defined in Table A9.1 or A9.3.' \


    def formula(buildings, period, parameters):
        is_single_phase_motor = buildings('new_product_is_single_phase_motor', period)
        is_eligible_type = buildings('new_product_is_eligible_type', period)
        return is_single_phase_motor * is_eligible_type


class new_product_is_single_phase_motor(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new product a single phase motor?'  # need to put in different kinds of motors


class new_product_is_eligible_type(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new product a single speed, dual speed, multiple speed' \
            ' or a variable speed pump unit?'  # need to put in enum for different speeds. is this needed?


class pump_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the input power for the pump, in W?'


class eligible_pump_input_power(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the pump power more than 100W and less than 2500W?'

    def formula(buildings, period, parameters):
        input_power = buildings('pump_input_power', period)
        condition_input_power = input_power > 100 and input_power < 2500
        return condition_input_power


class eligible_pump_input_type_and_power(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the pump an eligible type and does the pump have an input' \
            ' power of more than 100W and less than 2500W?'

    def formula(buildings, period, parameters):
        eligible_type = buildings('new_end_user_equipment_is_eligible_type', period)
        eligible_input_power = buildings('eligible_pump_input_power', period)
        return eligible_type * eligible_input_power


class StarRating(Enum):
    zero_point_five_stars = 'The pool pump has a rating of 0.5 stars.'
    one_star = 'The pool pump has a rating of 1 star.'
    one_point_five_stars = 'The pool pump has a rating of 1.5 stars.'
    two_stars = 'The pool pump has a rating of 2 stars.'
    two_point_five_stars = 'The pool pump has a rating of 2.5 stars.'
    three_stars = 'The pool pump has a rating of 3 stars.'
    three_point_five_stars = 'The pool pump has a rating of 3.5 stars.'
    four_stars = 'The pool pump has a rating of 4 stars.'
    four_point_five_stars = 'The pool pump has a rating of 4.5 stars.'
    five_stars = 'The pool pump has a rating of 5 stars.'
    five_point_five_stars = 'The pool pump has a rating of 5.5 stars.'
    six_stars = 'The pool pump has a rating of 6 stars.'
    seven_stars = 'The pool pump has a rating of 7 stars.'
    eight_stars = 'The pool pump has a rating of 8 stars.'
    nine_stars = 'The pool pump has a rating of 9 stars.'
    ten_stars = 'The pool pump has a rating of 10 stars.'  # I don't think this is good UX? - LM


class star_rating(Variable):
    value_type = Enum
    entity = Building
    definition_period = ETERNITY
    possible_values = StarRating
    default_value = StarRating.zero_point_five_stars
    label = 'What is the star rating for the relevant pool pump?'


class star_rating_above_minimum(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the star rating above the 4.5 minimum when determined in' \
            ' accordanc with AS5102.2?'

    def formula(buildings, period, parameters):
        star_rating = buildings('star_rating', period)
        return ((star_rating == four_point_five_stars) + (star_rating == five_stars)
               + (star_rating == five_point_five_stars) + (star_rating == six_stars)
               + (star_rating == seven_stars) + (star_rating == eight_stars)
               + (star_rating == nine_stars) + (star_rating == ten_stars))


class D5_warranty_length(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the warranty length of the pool pump, in years?'


class D5_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the pool pump has a minimum warranty length of' \
            ' 2 years, as required by Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('D5_warranty_length', period)
        return warranty_length >= 3
