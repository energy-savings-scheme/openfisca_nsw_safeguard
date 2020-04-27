# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class existing_lamp_is_linear_halogen_floodlight(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a linear halogen floodlight, as' \
            ' required in Eligiblity Requirement 1 in Activity Definition' \
            ' E2, and defined in Table A9.1.'  # insert definition requirements

    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('existing_lamp_type', period)
        EquipmentClassStatus = existing_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_tungsten_halogen_240V = (existing_lamp_type == EquipmentClassStatus.linear_halogen_floodlight)
        return is_tungsten_halogen_240V


class E2_existing_lamp_rating(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the rated wattage of the existing lamp.'  # need to check whether lamp rating is int or float


class existing_lamp_rating_is_more_than_100W(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp rating is 35W or 50W, as required' \
            ' in Eligibility Requirement 3 in Activity Definition E1.'  # insert definition requirements

    def formula(buildings, period, parameters):
        existing_lamp_rating = buildings('existing_lamp_rating', period)
        condition_lamp_rating = existing_lamp_rating > 100
        return condition_lamp_rating


class E2_is_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp and luminaire is in working order' \
            ' as required in Eligibility Requirement 3 in Activity Definition' \
            ' E1.'  # insert definition requirements


class E2_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'asks whether all of the eligiblity requirements for E2 have been' \
            ' successfully met.'

    def formula(buildings, period, parameters):
        is_linear_halogen_floodlight = buildings('existing_lamp_is_linear_halogen_floodlight', period)
        existing_lamp_more_than_100W = buildings('existing_lamp_rating_is_more_than_100W', period)
        existing_lamp_in_working_order = buildings('E2_is_in_working_order', period)
        return is_linear_halogen_floodlight * existing_lamp_more_than_100W * existing_lamp_in_working_order
