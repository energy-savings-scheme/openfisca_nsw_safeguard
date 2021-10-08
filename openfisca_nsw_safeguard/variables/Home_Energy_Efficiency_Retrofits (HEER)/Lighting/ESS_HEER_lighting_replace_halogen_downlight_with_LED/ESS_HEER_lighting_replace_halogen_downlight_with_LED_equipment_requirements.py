from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_HEER_lighting_replace_halogen_downlight_existing_end_user_equipment_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a LED Lamp only - ELV, an' \
            ' LED Lamp and Driver, an LED Luminaire-recessed or an LED Lamp' \
            ' only - 240V Self Ballasted, as required in Equipment Requirement' \
            ' 1 in Activity Definition E1, and defined in Table A9.1 or A9.3.' \

    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('ESS_HEER_lighting_existing_lamp_type', period)
        EquipmentClassStatus = existing_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_led_lamp_only_ELV = (existing_lamp_type == EquipmentClassStatus.LED_lamp_only_ELV)
        is_LED_lamp_and_driver = (existing_lamp_type == EquipmentClassStatus.LED_lamp_and_driver)
        is_LED_luminaire_recessed = (existing_lamp_type == EquipmentClassStatus.LED_luminaire_recessed)
        LED_lamp_only_240V_self_ballasted = (existing_lamp_type == EquipmentClassStatus.LED_luminaire_recessed)
        return is_led_lamp_only_ELV + is_LED_lamp_and_driver
        + is_LED_luminaire_recessed + LED_lamp_only_240V_self_ballasted


class ESS_HEER_lighting_replace_halogen_downlight_outputs_minimum_downward_light_output(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Assesses whether the minimum Download Light Output meets the' \
            ' requirement set out in Equipment Requirement 3 of Activity' \
            ' Definition E1.'

    def formula(buildings, period, parameters):
        download_light_output = buildings('ESS_HEER_downward_light_output', period)
        condition_minimum_light_output = download_light_output >= 462 # need to rewrite as parameter
        return condition_minimum_light_output


class ESS_HEER_lighting_replace_halogen_downlight_light_beam_angles_are_consistent(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new lamp has a beam angle consistent with the' \
            ' original lamp being replaced, as required by Equipment' \
            ' Requirement 4.'  # need to refer to IPART's method guide to define "consistent"

    def formula(buildings, period, parameters):
        original_light_beam_angle = buildings('ESS_HEER_original_light_beam_angle', period)
        new_light_beam_angle = buildings('ESS_HEER_new_light_beam_angle', period)
        light_beam_angles_are_consistent = (original_light_beam_angle == new_light_beam_angle)
        return light_beam_angles_are_consistent


class ESS_HEER_lighting_replace_halogen_downlight_is_compatible_with_circuit_dimmers(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'asks whether the new lamp is compatible with any dimmer installed' \
            ' on the same circuit as the new lamp.'


class ESS_HEER_lighting_replace_halogen_downlight_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Implementation meet all of the Activity Requirements for' \
            ' Activity Definition E1?'

    def formula(buildings, period, parameters):
        existing_equipment_is_eligible = buildings(
        'ESS_HEER_lighting_replace_halogen_downlight_existing_end_user_equipment_is_eligible', period
        )
        outputs_minimum_downward_light_output = buildings(
        'ESS_HEER_lighting_replace_halogen_downlight_outputs_minimum_downward_light_output', period
        )
        light_beam_angles_are_consistent = buildings(
        'ESS_HEER_lighting_replace_halogen_downlight_light_beam_angles_are_consistent', period
        )
        compatible_with_circuit_dimmers = buildings(
        'ESS_HEER_lighting_replace_halogen_downlight_is_compatible_with_circuit_dimmers', period
        )

        return (
        existing_equipment_is_eligible *
        outputs_minimum_downward_light_output *
        light_beam_angles_are_consistent *
        compatible_with_circuit_dimmers
        )
