# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class DR_AC_new_product_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the new air conditioner been installed?'
    # probably should link in w. 5.3 requirements, if needed. What does it mean \
    # to be installed?

class DR_AC_demand_response_enabling_device_installed_to_AC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has a demand response enabling device been installed to the' \
            ' air conditioner?'


class DR_AC_demand_response_enabling_device_connected_to_communication_network(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has a demand response enabling device been connected to the' \
            ' communication network?'


class DR_AC_demand_response_enabling_device_complies_with_AS_4775_1(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the demand response enabling device comply with AS 4775.1?'


class DR_AC_end_user_consents_to_demand_response_participation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the end user consent to participation in the relevant' \
            ' demand response program?'


class DR_AC_activity_is_performed_by_qualified_licence_holder(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity performed by a qualified licence holder?'
    # what licence? this is vague and unclear


class DR_AC_activity_is_supervised_by_qualified_licence_holder(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity supervised by a qualified licence holder?'
    # what licence? this is vague and unclear


class DR_AC_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Implementation' \
            ' Requirements defined in Activity Definition F4?'

    def formula(buildings, period, parameters):
        is_installed = buildings('DR_AC_new_product_is_installed', period)
        DRED_installed_to_AC = buildings('DR_AC_demand_response_enabling_device_installed_to_AC', period)
        DRED_connected_to_network = buildings('DR_AC_demand_response_enabling_device_connected_to_communication_network', period)
        DRED_complies_with_standards = buildings('DR_AC_demand_response_enabling_device_complies_with_AS_4775_1', period)
        user_consents_to_demand_response = buildings('DR_AC_end_user_consents_to_demand_response_participation', period)
        performed_by_licence_holder = buildings('activity_is_performed_by_qualified_licence_holder', period)
        supervised_by_licence_holder = buildings('activity_is_supervised_by_qualified_licence_holder', period)
        return (is_installed
        * (DRED_installed_to_AC * DRED_connected_to_network * DRED_complies_with_standards)
        * user_consents_to_demand_response
        * (performed_by_licence_holder + supervised_by_licence_holder))
