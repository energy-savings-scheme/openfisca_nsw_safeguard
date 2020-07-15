# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F4_product_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product installed?'
    # probably should link in w. 5.3 requirements, if needed. What does it mean \
    # to be installed?

class activity_is_performed_by_qualified_licence_holder(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity performed by a qualified licence holder?'
    # what licence? this is vague and unclear


class activity_is_supervised_by_qualified_licence_holder(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity supervised by a qualified licence holder?'
    # what licence? this is vague and unclear


class F4_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Implementation' \
            ' Requirements defined in Activity Definition F4?'

    def formula(buildings, period, parameters):
        is_installed = buildings('F4_product_is_installed', period)
        performed_by_licence_holder = buildings('activity_is_performed_by_qualified_licence_holder', period)
        supervised_by_licence_holder = buildings('activity_is_supervised_by_qualified_licence_holder', period)
        return is_installed * (performed_by_licence_holder + supervised_by_licence_holder)
