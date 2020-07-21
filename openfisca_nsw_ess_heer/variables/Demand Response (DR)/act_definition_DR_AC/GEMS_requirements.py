# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class DR_AC_GEMS_MEPS_requirement(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the AC complies with the relevant GEMS MEPS' \
            ' requirements for ACs without variable capacity, as defined' \
            ' in section 21 of the Greenhouse and Energy Minimum Standards' \
            ' (Air Conditioners up to 65kW) Determination 2019'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        MEPS_value = parameters(period).F4.MEPS_values[product_class]
        cooling_capacity = buildings('cooling_capacity', period)
        heating_capacity = buildings('heating_capacity', period)
        return where((cooling_capacity == 0),
                    (heating_capacity > MEPS_value),
                    (cooling_capacity > MEPS_value))
