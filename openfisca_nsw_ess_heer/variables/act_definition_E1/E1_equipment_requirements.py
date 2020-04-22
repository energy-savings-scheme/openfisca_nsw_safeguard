# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class new_end_user_equipment_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a LED Lamp only - ELV, an' \
            ' LED Lamp and Driver, an LED Luminaire-recessed or an LED Lamp' \
            ' only - 240V Self Ballasted, as required in Equipment Requirement' \
            ' 1 in Activity Definition E1, and defined in Table A9.1 or A9.3.' \


    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('existing_lamp_type', period)
        EquipmentClassStatus = existing_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_led_lamp_only_ELV = (existing_lamp_type == EquipmentClassStatus.LED_lamp_only_ELV)
        is_LED_lamp_and_driver = (existing_lamp_type == EquipmentClassStatus.LED_lamp_and_driver)
        is_LED_luminaire_recessed = (existing_lamp_type == EquipmentClassStatus.LED_luminaire_recessed)
        LED_lamp_only_240V_self_ballasted = (existing_lamp_type == EquipmentClassStatus.LED_luminaire_recessed)
        return is_led_lamp_only_ELV + is_LED_lamp_and_driver
        + is_LED_luminaire_recessed + LED_lamp_only_240V_self_ballasted


class downward_light_output(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'User input for the downward light output of the new End-User' \
            ' Equipment, in lumens.'


class outputs_minimum_downward_light_output(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Assesses whether the minimum Download Light Output meets the' \
            ' requirement set out in Equipment Requirement 3 of Activity' \
            ' Definition E1.'

    def formula(buildings, period, parameters):
        download_light_output = buildings('downward_light_output', period)
        condition_minimum_light_output = download_light_output >= 462
        return condition_minimum_light_output


class original_light_beam_angle(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'user input for the angle of the original lamp light beam.'


class new_light_beam_angle(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'user input for the angle of the new lamp light beam.'


class light_beam_angles_are_consistent(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new lamp has a beam angle consistent with the' \
            ' original lamp being replaced, as required by Equipment' \
            ' Requirement 4.'  # need to refer to IPART's method guide to define "consistent"

    def formula(buildings, period, parameters):
        original_light_beam_angle = buildings('original_light_beam_angle', period)
        new_light_beam_angle = buildings('new_light_beam_angle', period)
        light_beam_angles_are_consistent = (original_light_beam_angle == new_light_beam_angle)
        return light_beam_angles_are_consistent


class is_compatible_with_circuit_dimmers(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'asks whether the new lamp is compatible with any dimmer installed' \
            ' on the same circuit as the new lamp.'
