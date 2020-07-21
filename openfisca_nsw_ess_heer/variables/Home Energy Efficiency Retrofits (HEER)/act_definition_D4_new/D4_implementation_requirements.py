# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class D4_new_air_con_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the new air conditioner been installed by a qualified licence' \
            ' holder?'
    documentation = 'Variable X'


class D4_new_activity_is_performed_by_qualified_licence_holder(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity performed by a qualified licence holder?'
    # what licence? this is vague and unclear


class D4_new_activity_is_supervised_by_qualified_licence_holder(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity supervised by a qualified licence holder?'
    # what licence? this is vague and unclear


class D4_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the implementation meet the requirements outlined in' \
            ' Activity Definition D4?'
    documentation = 'Variable X'

    def formula(buildings, period, parameters):
        new_air_con_is_installed = buildings('D4_new_air_con_is_installed', period)
        performed_by_licence_holder = buildings('D4_new_activity_is_performed_by_qualified_licence_holder', period)
        supervised_by_licence_holder = buildings('D4_new_activity_is_supervised_by_qualified_licence_holder', period)
        return (new_air_con_is_installed * (performed_by_licence_holder + supervised_by_licence_holder))
