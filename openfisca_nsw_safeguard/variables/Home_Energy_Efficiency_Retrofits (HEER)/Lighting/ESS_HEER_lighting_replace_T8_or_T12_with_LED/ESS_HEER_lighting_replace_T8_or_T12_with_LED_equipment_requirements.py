from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_lighting_replace_T8_or_T12_with_LED_new_end_user_equipment_is_LED_linear_lamp(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new lamp is a LED linear lamp' \
            ' luminaire, as required in Equipment Requirement' \
            ' 1 in Activity Definition E1, and defined in Table A9.1 or A9.3.' \


    def formula(buildings, period, parameters):
        new_lamp_type = buildings('ESS_HEER_lighting_new_lamp_type', period)
        EquipmentClassStatus = new_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_LED_linear = (new_lamp_type == EquipmentClassStatus.LED_luminaire_linear_lamp)
        return is_LED_linear


class ESS_HEER_lighting_replace_T8_or_T12_with_LED_is_not_retrofit_or_modified(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a Retrofit LED Linear Lamp' \
            ' or a Modified LED Linear Lamp.' \

    def formula(buildings, period, parameters):
        new_lamp_type = buildings('ESS_HEER_lighting_new_lamp_type', period)
        EquipmentClassStatus = new_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_retrofit_LED_linear = (new_lamp_type == EquipmentClassStatus.retrofit_luminaire_LED_linear_lamp)
        is_modified_LED_linear = (new_lamp_type == EquipmentClassStatus.modified_luminaire_LED_linear_lamp)
        return not(is_retrofit_LED_linear + is_modified_LED_linear)


class ESS_HEER_lighting_replace_T8_or_T12_with_LED_meets_A9_4_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the End User Equipment meets the requirements of' \
            ' table A9.4, as required by Equipment Requirement 2.'


class ESS_HEER_lighting_replace_T8_or_T12_with_LED_minimum_lamp_life(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether, if the replacement light is a CFLi, whether it' \
            ' meets the 20,000 hour minimum requirement as required by' \
            ' Equipment requirement 3.'

    def formula(buildings, period, parameters):
        new_lamp_life = buildings('ESS_HEER_new_lamp_life', period)
        condition_new_lamp_life = new_lamp_life >= 20000 # rewrite as parameter
        return condition_new_lamp_life


class ESS_HEER_lighting_replace_T8_or_T12_with_LED_is_compatible_with_circuit_dimmers(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'asks whether the new lamp is compatible with any dimmer installed' \
            ' on the same circuit as the new lamp.'


class ESS_HEER_lighting_replace_T8_or_T12_with_LED_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the implementation meets the Equipment Requirements' \
            ' detailed in Activity Definition E5.'

    def formula(buildings, period, parameters):
        new_equipment_is_LED_linear_lamp = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_with_LED_new_end_user_equipment_is_LED_linear_lamp', period
        )
        is_not_retrofit_or_modified = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_with_LED_is_not_retrofit_or_modified', period
        )
        meets_9_4_requirements = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_with_LED_meets_A9_4_requirements', period
        )
        has_minimum_lamp_life = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_with_LED_minimum_lamp_life', period
        )
        is_ciruit_dimmer_compatible = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_with_LED_is_compatible_with_circuit_dimmers', period)
        return(
        new_equipment_is_LED_linear_lamp *
        is_not_retrofit_or_modified *
        meets_9_4_requirements *
        has_minimum_lamp_life *
        is_ciruit_dimmer_compatible
        )
