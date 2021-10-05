from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_lighting_replace_T8_or_T12_w_T5_new_end_user_equipment_is_T5_linear(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a T5 linear fluoroescent' \
            ' luminaire, as required in Equipment Requirement' \
            ' 1 in Activity Definition E1, and defined in Table A9.1 or A9.3.' \


    def formula(buildings, period, parameters):
        new_lamp_type = buildings('ESS_HEER_lighting_new_lamp_type', period)
        EquipmentClassStatus = new_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_T5_linear = (new_lamp_type == EquipmentClassStatus.T5_linear)
        return is_T5_linear


class ESS_HEER_lighting_replace_T8_or_T12_w_T5_not_T5_adaptor_kit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a T5 adaptor kit fixed to a' \
            ' luminaire, as this is not allowed in Equipment Requirement' \
            ' 1 in Activity Definition E1, and defined in Table A9.1 or A9.3.'

    def formula(buildings, period, parameters):
        new_lamp_type = buildings('ESS_HEER_lighting_new_lamp_type', period)
        EquipmentClassStatus = new_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_T5_adaptor_kit = (new_lamp_type == EquipmentClassStatus.T5_adaptor_kit)
        return not(is_T5_adaptor_kit)


class ESS_HEER_lighting_replace_T8_or_T12_w_T5__minimum_lamp_life(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether, if the replacement light is a CFLi, whether it' \
            ' meets the 20,000 hour minimum requirement as required by' \
            ' Equipment requirement 3.'

    def formula(buildings, period, parameters):
        new_lamp_life = buildings('ESS_HEER_new_lamp_life', period)
        condition_new_lamp_life = new_lamp_life >= 20000
        return condition_new_lamp_life


class ESS_HEER_lighting_replace_T8_or_T12_w_T5_new_lamp_length_consistent_with_existing_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new lamp length is consistent with the existing' \
            ' lamp length, as required in Equipment Requirement 3 of Activity' \
            ' Definition E4.'

    def formula(buildings, period, parameters):
        existing_lamp_length = buildings('ESS_HEER_existing_lamp_length', period)
        new_lamp_length = buildings('ESS_HEER_new_lamp_length', period)
        condition_same_length = (existing_lamp_length == new_lamp_length)
        return condition_same_length


class ESS_HEER_lighting_replace_T8_or_T12_w_T5_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the implementation meets the Equipment Requirements' \
            ' detailed in Activity Definition E4.'

    def formula(buildings, period, parameters):
        new_equipment_is_T5 = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_w_T5_new_end_user_equipment_is_T5_linear', period)
        new_equipment_is_not_T5_adaptor = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_w_T5_not_T5_adaptor_kit', period)
        has_minimum_lamp_life = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_w_T5__minimum_lamp_life', period
        )
        has_consistent_lamp_length = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_w_T5_new_lamp_length_consistent_with_existing_length', period
        )
        return(
        new_equipment_is_T5 *
        new_equipment_is_not_T5_adaptor *
        has_minimum_lamp_life *
        has_consistent_lamp_length
        )
