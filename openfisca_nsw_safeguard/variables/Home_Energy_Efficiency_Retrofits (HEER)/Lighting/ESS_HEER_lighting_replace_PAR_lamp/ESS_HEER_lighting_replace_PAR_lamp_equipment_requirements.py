from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_lighting_replace_PAR_lamp_new_end_user_equipment_is_eligible(Variable):
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
        is_LED_lamp_only_240V_self_ballasted = (existing_lamp_type == EquipmentClassStatus.LED_lamp_only_240V_self_ballasted)
        is_CFLi = (existing_lamp_type == EquipmentClassStatus.CFLi)
        is_LED_luminaire_floodlight = (existing_lamp_type == EquipmentClassStatus.LED_luminaire_floodlight)
        return is_LED_lamp_only_240V_self_ballasted + is_CFLi + is_LED_luminaire_floodlight


class ESS_HEER_lighting_replace_PAR_lamp_meets_A9_4_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the End User Equipment meets the requirements of' \
            ' table A9.4, as required by Equipment Requirement 2.'


class ESS_HEER_lighting_replace_PAR_lamp_minimum_lamp_life(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether, if the replacement light is a CFLi, whether it' \
            ' meets the 10,000 hour minimum requirement as required by' \
            ' equipment requirement 3.'

    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('ESS_HEER_lighting_existing_lamp_type', period)
        is_CFLi = (existing_lamp_type == EquipmentClassStatus.CFLi)
        is_LED_lamp_only_240V_self_ballasted = (existing_lamp_type == EquipmentClassStatus.LED_lamp_only_240V_self_ballasted)
        is_LED_luminaire_floodlight = (existing_lamp_type == EquipmentClassStatus.LED_luminaire_floodlight)
        new_lamp_life = buildings('ESS_HEER_new_lamp_life', period)
        condition_new_lamp_life = new_lamp_life >= 10000
        return (is_CFLi * condition_new_lamp_life) + is_LED_lamp_only_240V_self_ballasted + is_LED_luminaire_floodlight


class ESS_HEER_lighting_replace_PAR_lamp_light_beam_angles_are_consistent(Variable):
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


class ESS_HEER_lighting_replace_PAR_lamp_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Implementation satisfy the Equipment Requirements detailed in' \
            ' Activity Definition E3?'

    def formula(buildings, period, parameters):
        new_equipment_is_eligible = buildings(
        'ESS_HEER_lighting_replace_PAR_lamp_new_end_user_equipment_is_eligible', period)
        meets_A9_4_requirements = buildings(
        'ESS_HEER_lighting_replace_PAR_lamp_meets_A9_4_requirements', period)
        has_minimum_lamp_life = buildings(
        'ESS_HEER_lighting_replace_PAR_lamp_minimum_lamp_life', period)
        light_beam_angles_are_consistent = buildings(
        'ESS_HEER_lighting_replace_PAR_lamp_light_beam_angles_are_consistent', period)
        return(
        new_equipment_is_eligible *
        meets_A9_4_requirements *
        has_minimum_lamp_life *
        light_beam_angles_are_consistent
        )
