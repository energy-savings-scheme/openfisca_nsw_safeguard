# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class existing_air_con_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing air conditioner in working order?'


class D3_meets_all_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the eligibility requirements?'

    def formula(buildings, period, parameters):
        in_working_order = buildings('existing_air_con_in_working_order', period)
        return in_working_order
