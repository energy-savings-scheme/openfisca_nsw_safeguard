from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_lighting_replace_PAR_lamp_existing_lamp_is_240V_PAR(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a 240V parabolic aluminised' \
            ' reflector lamp, as required in Eligiblity Requirement 1 in' \
            ' Activity Definition E3, and defined in Table A9.1.'  # this light type is not defined anywhere in the rule (and probably should be!)

    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('ESS_HEER_lighting_existing_lamp_type', period)
        EquipmentClassStatus = existing_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_240V_PAR = (existing_lamp_type == EquipmentClassStatus.PAR)
        return is_240V_PAR


class ESS_HEER_lighting_replace_PAR_lamp_existing_lamp_rating_more_than_80W_less_than_160W(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp rating more than 80W and less than 160W.'

    def formula(buildings, period, parameters):
        existing_lamp_rating = buildings('ESS_HEER_existing_lamp_rating', period)
        return ((existing_lamp_rating > 80) * (existing_lamp_rating < 160))


class ESS_HEER_lighting_replace_PAR_lamp_is_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp and luminaire is in working order' \
            ' as required in Eligibility Requirement 3 in Activity Definition' \
            ' E1.'  # insert definition requirements


class ESS_HEER_lighting_replace_PAR_lamp_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the implementation meets the Implementation Requirements' \
            ' detailed in Activity Definition E3.'
