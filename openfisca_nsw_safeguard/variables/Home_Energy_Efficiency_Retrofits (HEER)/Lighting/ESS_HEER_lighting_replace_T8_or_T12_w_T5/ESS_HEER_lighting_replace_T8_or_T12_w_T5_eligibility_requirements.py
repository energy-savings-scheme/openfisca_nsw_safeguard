from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_lighting_replace_T8_or_T12_w_T5_existing_lamp_is_T8_or_T12_fluoro_luminaire(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a 2 foot, 3 foot, 4 foot,' \
            ' or 5 foot T8 or T12 fluorescent reflector lamp, as required' \
            ' in Eligiblity Requirement 1 in Activity Definition E4,' \
            ' and defined in Table A9.1.'  # this light type is not defined anywhere in the rule (and probably should be!)

    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('ESS_HEER_lighting_existing_lamp_type', period)
        EquipmentClassStatus = existing_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_T12_linear = (existing_lamp_type == EquipmentClassStatus.T12_linear)
        is_T8_linear = (existing_lamp_type == EquipmentClassStatus.T8_linear)  # please advise if T8 circulars are to be included as well
        return is_T12_linear + is_T8_linear  # note addition is used to define "or" with booleans


class ESS_HEER_lighting_replace_T8_or_T12_w_T5_is_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp and luminaire is in working order' \
            ' as required in Eligibility Requirement 3 in Activity Definition' \
            ' E1.'  # insert definition requirements


class ESS_HEER_lighting_replace_T8_or_T12_w_T5_is_not_modified_with_T5_adaptor_kit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is modified with a T5 adaptor kit,' \
            ' as this is not allowed within Eligibility Requirement 2 in' \
            ' in Activity Definition E4 and defined in Table A9.1.'  # this light type is not defined anywhere in the rule (and probably should be!)


class ESS_HEER_lighting_replace_T8_or_T12_w_T5_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Implementation meet the Implementation Requirements in' \
            ' Activity Definition E4?'

    def formula(buildings, period, parameters):
        existing_lamp_is_T8_or_T12 = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_w_T5_existing_lamp_is_T8_or_T12_fluoro_luminaire', period)
        existing_lamp_in_working_order = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_w_T5_is_in_working_order', period)
        not_modified_with_T5_adaptor = buildings(
        'ESS_HEER_lighting_replace_T8_or_T12_w_T5_is_not_modified_with_T5_adaptor_kit', period)
        return(
        existing_lamp_is_T8_or_T12 *
        existing_lamp_in_working_order *
        not_modified_with_T5_adaptor
        )
