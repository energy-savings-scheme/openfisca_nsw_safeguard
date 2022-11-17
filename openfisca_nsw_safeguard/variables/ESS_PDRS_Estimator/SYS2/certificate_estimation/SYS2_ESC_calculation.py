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
    #New End-User Equipment must achieve a minimum 4.5 star rating to be eligible
    four_and_a_half_stars = '4.5 stars'
    five_stars = '5 stars'
    five_and_a_half_stars = '5.5 stars'
    six_stars = '6 stars'
    six_and_a_half_stars = '6.5 stars'
    seven_stars = '7 stars'
    seven_and_a_half_stars = '7.5 stars'
    eight_stars = '8 stars'
    eight_and_a_half_stars = '8.5 stars'
    nine_stars = '9 stars'
    nine_and_a_half_stars = '9.5 stars'
    ten_stars = '10 stars'


class SYS2_star_rating(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS2StarRating
    default_value = SYS2StarRating.five_and_a_half_stars
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'New equipment star rating',
        'display_question' : 'What is the star rating of your new equipment? (Equipment must achieve a 4.5 star rating or higher)',
        'sorting' : 5
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
        replacement_activity = buildings('SYS2_Replacement_Activity', period)
        
        SYS2_eligible_ESCs = np.select(
            [
                replacement_activity,
                np.logical_not(replacement_activity)
            ],
            [
                (electricity_savings * electricity_certificate_conversion_factor),
                0
            ])

        result_to_return = np.select(
            [
                SYS2_eligible_ESCs <= 0, SYS2_eligible_ESCs > 0
            ],
            [
                0, SYS2_eligible_ESCs
            ])
        return result_to_return