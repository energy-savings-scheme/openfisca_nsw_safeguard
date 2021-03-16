# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E4_new_end_user_equipment_is_T5_linear(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a T5 linear fluoroescent' \
            ' luminaire, as required in Equipment Requirement' \
            ' 1 in Activity Definition E1, and defined in Table A9.1 or A9.3.' \


    def formula(buildings, period, parameters):
        new_lamp_type = buildings('new_lamp_type', period)
        EquipmentClassStatus = new_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_T5_linear = (new_lamp_type == EquipmentClassStatus.T5_linear)
        return is_T5_linear


class is_not_T5_adaptor_kit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a T5 adaptor kit fixed to a' \
            ' luminaire, as this is not allowed in Equipment Requirement' \
            ' 1 in Activity Definition E1, and defined in Table A9.1 or A9.3.'

    def formula(buildings, period, parameters):
        new_lamp_type = buildings('new_lamp_type', period)
        EquipmentClassStatus = new_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_T5_adaptor_kit = (new_lamp_type == EquipmentClassStatus.T5_adaptor_kit)
        return not(is_T5_adaptor_kit)


class E4_new_lamp_life(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'measures the Lamp Life of the replacement light in hours'


class E4_minimum_lamp_life(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether, if the replacement light is a CFLi, whether it' \
            ' meets the 20,000 hour minimum requirement as required by' \
            ' Equipment requirement 3.'

    def formula(buildings, period, parameters):
        new_lamp_life = buildings('E3_new_lamp_life', period)
        condition_new_lamp_life = new_lamp_life >= 20000
        return condition_new_lamp_life


class new_lamp_length(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the length of the new lamp in feet.'  # need to check if there's set lengths for these, and if so, redefine as an enum


class new_lamp_length_consistent_with_existing_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new lamp length is consistent with the existing' \
            ' lamp length, as required in Equipment Requirement 3 of Activity' \
            ' Definition E4.'

    def formula(buildings, period, parameters):
        existing_lamp_length = buildings('existing_lamp_length', period)
        new_lamp_length = buildings('new_lamp_length', period)
        condition_same_length == (existing_lamp_length == new_lamp_length)
        return condition_same_length
