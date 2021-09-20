from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_SONA_freezer_refrigerator_is_in_eligible_group(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment in Refrigerator Group 4, 5B, 5S or 5T?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B5, Equipment Requirement 1.'

    def formula(buildings, period, parameters):
        refrigerator_group = buildings('refrigerator_or_freezer_group', period)
        RefrigeratorGroup = refrigerator_group.possible_values  # imports functionality of refrigerator group enum from user_inputs
        in_group_6C = (refrigerator_group == RefrigeratorGroup.group_6C)
        in_group_6U = (refrigerator_group == RefrigeratorGroup.group_6U)
        in_group_7 = (refrigerator_group == RefrigeratorGroup.group_7)
        return in_group_6C + in_group_6U + in_group_7


class ESS_SONA_freezer_end_user_equipment_is_labelled_for_energy_labelling(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment registered for energy labelling?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 2.'


class ESS_SONA_freezer_end_user_equipment_has_registered_volume(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment have a total volume,' \
            ' recorded in the GEMS Registry?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        refrigerator_volume = buildings('refrigerator_or_freezer_capacity', period)
        condition_volume_is_not_zero = ((refrigerator_volume != 0) and (refrigerator_volume != 0.0)
        and (refrigerator_volume is not None))
        return condition_volume_is_not_zero


class ESS_SONA_freezer_meets_all_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet all of the Equipment' \
            ' Requirements detailed in Activity Definition B1?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1.'

    def formula(buildings, period, parameters):
        in_eligible_group = buildings('ESS_SONA_freezer_refrigerator_is_in_eligible_group', period)
        is_labelled_for_energy_labelling = buildings('ESS_SONA_freezer_end_user_equipment_is_labelled_for_energy_labelling', period)
        has_volume = buildings('ESS_SONA_freezer_end_user_equipment_has_registered_volume', period)
        return (in_eligible_group * is_labelled_for_energy_labelling * has_volume)
