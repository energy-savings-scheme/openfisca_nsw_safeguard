# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class D18_b_existing_end_user_equipment_is_disconnected(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the existing End User Equipment been disconnected?'


class D18_b_existing_end_user_equipment_is_removed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the existing End User Equipment been removed?'


class D18_b_existing_EUE_is_disconnected_and_removed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the existing End User Equipment been disconnected and removed?'

    def formula(buildings, period, parameters):
        has_been_disconnected = buildings('D18_b_existing_end_user_equipment_is_disconnected', period)
        has_been_removed = buildings('D18_b_existing_end_user_equipment_is_removed', period)
        return has_been_disconnected * has_been_removed


class D18_b_new_EUE_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the new End User Equipment been installed?'


class D18_b_activity_is_performed_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity performed by a qualified person, in accordance' \
            ' the new End User Equipment installation requirements, and in' \
            ' compliance with the relevant plumbing standards, Gas work ' \
            ' standards, electrical work standards and permanent wiring' \
            ' standards?'


class D18_b_activity_is_supervised_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity supervised by a qualified person, in accordance' \
            ' the new End User Equipment installation requirements, and in' \
            ' compliance with the relevant plumbing standards, Gas work ' \
            ' standards, electrical work standards and permanent wiring' \
            ' standards?'


class D18_b_activity_is_performed_or_supervised_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity supervised by a qualified person, in accordance' \
            ' the new End User Equipment installation requirements, and in' \
            ' compliance with the relevant plumbing standards, Gas work ' \
            ' standards, electrical work standards and permanent wiring' \
            ' standards?'

    def formula(buildings, period, parameters):
        performed_by_qualified_person = buildings('D18_b_activity_is_performed_by_qualified_person', period)
        supervised_by_qualified_person = buildings('D18_b_activity_is_supervised_by_qualified_person', period)
        return (performed_by_qualified_person + supervised_by_qualified_person)


class D18_b_meets_all_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the equipment requirements detailed' \
            ' in Activity Definition F16 - version A?'

    def formula(buildings, period, parameters):
        existing_equipment_disconnected_and_removed = buildings('D18_b_existing_EUE_is_disconnected_and_removed', period)
        new_equipment_installed = buildings('D18_b_new_EUE_is_installed', period)
        performed_or_supervised_by_qualified_person = buildings('D18_b_activity_is_performed_or_supervised_by_qualified_person', period)
        return (existing_equipment_disconnected_and_removed * new_equipment_installed * performed_or_supervised_by_qualified_person)
