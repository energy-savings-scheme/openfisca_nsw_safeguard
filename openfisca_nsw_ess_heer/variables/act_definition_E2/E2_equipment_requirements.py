# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E2_new_end_user_equipment_is_eligible(Variable):
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
        is_CFLi = (existing_lamp_type == EquipmentClassStatus.CFLi)
        is_LED_luminaire_floodlight = (existing_lamp_type == EquipmentClassStatus.LED_luminaire_floodlight)
        return is_CFLi + is_LED_luminaire_floodlight


class meets_A9_4_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the End User Equipment meets the requirements of' \
            ' table A9.4, as required by Equipment Requirement 2.'


class new_lamp_life(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'measures the Lamp Life of the replacement light in hours'


class minimum_lamp_life(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether, if the replacement light is a CFLi, whether it' \
            ' meets the 10,000 hour minimum requirement as required by' \
            ' equipment requirement 3.'

    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('existing_lamp_type', period)
        is_CFLi = (existing_lamp_type == EquipmentClassStatus.CFLi)
        is_LED_luminaire_floodlight = (existing_lamp_type == EquipmentClassStatus.LED_luminaire_floodlight)
        new_lamp_life = buildings('new_lamp_life', period)
        condition_new_lamp_life = new_lamp_life >= 10000
        return (is_CFLi * condition_new_lamp_life) + is_LED_luminaire_floodlight


class E2_original_light_beam_angle(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'user input for the angle of the original lamp light beam.'


class E2_new_light_beam_angle(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'user input for the angle of the new lamp light beam.'


class E2_light_beam_angles_are_consistent(Variable):
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
