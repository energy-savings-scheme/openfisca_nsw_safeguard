# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class D5_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new pool' \
            ' pump.'

    def formula(buildings, period, parameters):
        star_rating = buildings('star_rating', period)
        electricity_savings_factor = (parameters(period).table_D5_1.electricity_savings_factor[star_rating])
        return electricity_savings_factor
