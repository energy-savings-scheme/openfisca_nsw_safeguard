from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS_HEER_modify_external_window_with_draught_proofing_windows_have_gaps_between_door_and_frame(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Windows to be draught-proofed must have gaps between the door and' \
            ' frame and/or threshold that permit the infiltration of air into' \
            ' or out of the Site. Prescribed by Equipment Requirement 1 of' \
            ' Energy Savings Scheme Rule 2020.'  # IPART to define what this means and how to measure this


class ESS_HEER_modify_external_window_with_draught_proofing_window_is_external(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Only external doors may be draught-proofed. Prescribed by' \
            ' Equipment Requirement 1 of Energy Savings Scheme Rule 2020.'


class ESS_HEER_modify_external_window_with_draught_proofing_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Implementation meet the Eligibility Requirements defined' \
            ' in Activity Definition E8?'

    def formula(buildings, period, parameters):
        windows_have_gaps = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_windows_have_gaps_between_door_and_frame',
            period)
        windows_are_external = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_window_is_external',
            period)
        return (
            windows_have_gaps *
            windows_are_external
                )