from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS_HEER_pool_pump_replace_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new pool' \
            ' pump.'

    def formula(buildings, period, parameters):
        star_rating = buildings('ESS_HEER_pool_pump_star_rating', period)
        electricity_savings_factor = (parameters(period).
        ESS.HEER.table_D5_1.electricity_savings_factor[star_rating])
        return electricity_savings_factor


class PoolPumpStarRating(Enum):
    zero_stars = u'New pool pump has a Star Rating of 0 stars.'
    one_star = u'New pool pump has a Star Rating of 1 star.'
    one_and_a_half_stars = u'New pool pump has a Star Rating of 1.5 stars.'
    two_stars = u'New pool pump has a Star Rating of 2 stars.'
    two_and_a_half_stars = u'New pool pump has a Star Rating of 2.5 stars.'
    three_stars = u'New pool pump has a Star Rating of 3 stars.'
    three_and_a_half_stars = u'New pool pump has a  Star Rating of 3.5 stars.'
    four_stars = u'New pool pump has a Star Rating of 4 stars.'
    four_and_a_half_stars = u'New pool pump has a Star Rating of 4.5 stars.'
    five_stars = u'New pool pump has a Star Rating of 5 stars.'
    five_and_a_half_stars = u'New pool pump has a Star Rating of 5.5 stars.'
    six_stars = u'New pool pump has a Star Rating of 6 stars.'
    seven_stars = u'New pool pump has a Star Rating of 7 stars.'
    eight_stars = u'New pool pump has a Star Rating of 8 stars.'
    nine_stars = u'New pool pump has a Star Rating of 9 stars.'
    ten_stars = u'New pool pump has a Star Rating of 10 stars.'


class ESS_HEER_pool_pump_star_rating(Variable):
    value_type = Enum
    possible_values = PoolPumpStarRating
    default_value = PoolPumpStarRating.one_star
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new pool' \
            ' pump.'
