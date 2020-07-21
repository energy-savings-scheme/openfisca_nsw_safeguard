# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class D3_new_existing_air_con_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is there an existing air conditioner installed at the site?'


class D3_new_meets_all_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the eligibility requirements?'

    def formula(buildings, period, parameters):
        existing_installed_air_con = buildings('existing_air_con_is_installed', period)
        return existing_installed_air_con
