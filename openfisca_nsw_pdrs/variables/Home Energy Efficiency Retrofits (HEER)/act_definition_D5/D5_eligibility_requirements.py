# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

#  need to build logic through Enum to ask whether a door or window is being replaced


class existing_pool_pump_is_present(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is there an existing pool pump present at the Site?'


class D5_all_eligibility_requirements_are_true(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the eligibility requirements?'

    def formula(buildings, period, parameters):
        existing_pool_pump_is_present = buildings('existing_pool_pump_is_present', period)
        return existing_pool_pump_is_present
