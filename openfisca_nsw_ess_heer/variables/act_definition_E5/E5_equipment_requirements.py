# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E5_new_end_user_equipment_is_LED_linear_lamp(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a T5 linear fluoroescent' \
            ' luminaire, as required in Equipment Requirement' \
            ' 1 in Activity Definition E1, and defined in Table A9.1 or A9.3.' \


    def formula(buildings, period, parameters):
        new_lamp_type = buildings('new_lamp_type', period)
        EquipmentClassStatus = new_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_LED_linear = (new_lamp_type == EquipmentClassStatus.LED_luminaire_linear_lamp)
        return is_LED_linear


class E5_is_not_retrofit_or_modified(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a T5 adaptor kit fixed to a' \
            ' luminaire, as this is not allowed in Equipment Requirement' \
            ' 1 in Activity Definition E1, and defined in Table A9.1 or A9.3.' \

    def formula(buildings, period, parameters):
        new_lamp_type = buildings('new_lamp_type', period)
        EquipmentClassStatus = new_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_retrofit_LED_linear = (new_lamp_type == EquipmentClassStatus.retrofit_luminaire_LED_linear_lamp)
        is_modified_LED_linear = (new_lamp_type == EquipmentClassStatus.modified_luminaire_LED_linear_lamp)
        return not(is_retrofit_LED_linear + is_modified_LED_linear)


class E5_meets_A9_4_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the End User Equipment meets the requirements of' \
            ' table A9.4, as required by Equipment Requirement 2.'


class E5_new_lamp_life(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'measures the Lamp Life of the replacement light in hours'


class E5_minimum_lamp_life(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether, if the replacement light is a CFLi, whether it' \
            ' meets the 20,000 hour minimum requirement as required by' \
            ' Equipment requirement 3.'

    def formula(buildings, period, parameters):
        new_lamp_life = buildings('E5_new_lamp_life', period)
        condition_new_lamp_life = new_lamp_life >= 20000
        return condition_new_lamp_life


class E5_is_compatible_with_circuit_dimmers(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'asks whether the new lamp is compatible with any dimmer installed' \
            ' on the same circuit as the new lamp.'
