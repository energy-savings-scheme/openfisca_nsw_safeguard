from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_modify_door_draught_proofing_doors_have_gaps_between_door_and_frame(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Doors to be draught-proofed must have gaps between the door and' \
            ' frame and/or threshold that permit the infiltration of air into' \
            ' or out of the Site. Prescribed by Equipment Requirement 1 of' \
            ' Energy Savings Scheme Rule 2020.'  # IPART to define what this means and how to measure this


class ESS_HEER_modify_door_draught_proofing_door_is_external(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Only external doors may be draught-proofed. Prescribed by' \
            ' Equipment Requirement 1 of Energy Savings Scheme Rule 2020.'


class ESS_HEER_modify_door_draught_proofing_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the Implementation meets the Eligibility Requirements' \
            ' detailed in Activity Definition E7.'

    def formula(buildings, period, parameters):
        has_gaps_between_door_frame = buildings(
        'ESS_HEER_modify_door_draught_proofing_doors_have_gaps_between_door_and_frame', period)
        is_external_door = buildings(
        'ESS_HEER_modify_door_draught_proofing_door_is_external', period)
        return (has_gaps_between_door_frame *
                is_external_door)
