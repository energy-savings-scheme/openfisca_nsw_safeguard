from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class SYS2_PDRS__regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'
    metadata = {
        "variable-type": "inter-interesting",
        "alias":"PDRS Regional Network Factor",
        "display_question": "PDRS regional network factor"
    }

    def formula(buildings, period, parameters):
        postcode = buildings('SYS2_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided


class SYS2StarRating(Enum):
    zero_star = 'Zero stars'
    one_star = 'One star'
    one_and_a_half_stars = 'One and half stars'
    two_stars = 'Two stars'
    two_and_a_half_stars = 'Two and half stars'
    three_stars = 'Three stars'
    three_and_a_half_stars = 'Three and a half stars'
    four_stars = 'Four stars'
    four_and_a_half_stars = 'Four and a half stars'
    five_stars = 'Five stars'
    five_and_a_half_stars = 'Five and a half stars'
    six_stars = 'Six stars'
    six_and_a_half_stars = 'Six and a half stars'
    seven_stars = 'Seven stars'
    seven_and_a_half_stars = 'Seven and a half stars'
    eight_stars = 'Eight stars'
    eight_and_a_half_stars = 'Eight and a half stars'
    nine_stars = 'Nine stars'
    nine_and_a_half_stars = 'Nine and a half stars'
    ten_stars = "Ten stars"


class SYS2_star_rating(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS2StarRating
    default_value = SYS2StarRating.four_stars
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Star rating',
        'display_question' : 'What is the star rating of your pool pump?',
        'sorting' : 4
    }


class SYS2_savings_factor(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
        star_rating = buildings('SYS2_star_rating', period)
        savings_factor = parameters(period).ESS.HEER.table_D5_1['electricity_savings_factor'][star_rating]

        return savings_factor


class SYS2_electricity_savings(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('SYS2_savings_factor', period)
        regional_network_factor = buildings('SYS2_PDRS__regional_network_factor', period)

        electricity_savings = deemed_electricity_savings * regional_network_factor
        return electricity_savings


class SYS2_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'output',
        'label' : 'The number of ESCs for SYS2'
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('SYS2_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        #there is no gas option for this activity

        result = np.rint(electricity_savings * electricity_certificate_conversion_factor)
        result_to_return = np.select([
                result < 0, result > 0
            ], [
                0, result
            ])
        return result_to_return