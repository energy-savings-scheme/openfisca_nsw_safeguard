# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F1_2_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment installed?'

    def formula(buildings, period, parameters):
        in_intended_place_of_use = buildings('F1_2_is_in_intended_place_of_use', period)
        is_operating = buildings('F1_2_is_operating', period)


class F1_2_is_in_intended_place_of_use(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment in its intended place of use?'


class F1_2_is_operating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment operating?'


class F1_2_meets_installation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Installation meet all of the Installation Requirements?'

    def formula(buildings, period, parameters):
        is_installed = buildings('F1_2_is_installed', period)
        in_intended_place_of_use = buildings('F1_2_is_in_intended_place_of_use', period)
        is_operating = buildings('F1_2_is_operating', period)
        return is_installed * in_intended_place_of_use * is_operating
