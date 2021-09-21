from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class D5_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new pool' \
            ' pump.'

    def formula(buildings, period, parameters):
        star_rating = buildings('star_rating', period)
        electricity_savings_factor = (parameters(period).table_D3.electricity_savings_factor[star_rating])
        return electricity_savings_factor
