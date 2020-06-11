# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E4_existing_lamp_is_T8_or_T12_fluoro_luminaire(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a 2 foot, 3 foot, 4 foot,' \
            ' or 5 foot T8 or T12 fluorescent reflector lamp, as required' \
            ' in Eligiblity Requirement 1 in Activity Definition E4,' \
            ' and defined in Table A9.1.'  # this light type is not defined anywhere in the rule (and probably should be!)

    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('existing_lamp_type', period)
        EquipmentClassStatus = existing_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_T12_linear = (existing_lamp_type == EquipmentClassStatus.T12_linear)
        is_T8_linear = (existing_lamp_type == EquipmentClassStatus.T8_linear)  # please advise if T8 circulars are to be included as well
        return is_T12_linear + is_T8_linear  # note addition is used to define "or" with booleans


class E4_is_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp and luminaire is in working order' \
            ' as required in Eligibility Requirement 3 in Activity Definition' \
            ' E1.'  # insert definition requirements


class E4_is_not_modified_with_T5_adaptor_kit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is modified with a T5 adaptor kit,' \
            ' as this is not allowed within Eligibility Requirement 2 in' \
            ' in Activity Definition E4 and defined in Table A9.1.'  # this light type is not defined anywhere in the rule (and probably should be!)


class existing_lamp_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the length of the existing lamp in feet.'  # need to check if there's set lengths for these, and if so, redefine as an enum


class eligible_existing_lamp_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is 2 foot, 3 foot, 4 foot or 5 foot,' \
            ' as these are the only existing lights eligible to be replaced' \
            ' in Activity Definition E4.'  # this light type is not defined anywhere in the rule (and probably should be!)

    def formula(buildings, period, parameters):
        existing_lamp_length = buildings('existing_lamp_length', period)
        condition_eligible_length = (existing_lamp_length == 2 or existing_lamp_length == 3
                                    or existing_lamp_length == 4 or existing_lamp_length == 5)
        return condition_eligible_length
