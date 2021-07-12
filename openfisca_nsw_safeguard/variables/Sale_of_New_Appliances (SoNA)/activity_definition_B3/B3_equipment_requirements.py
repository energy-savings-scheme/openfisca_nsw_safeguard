from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS__SONA_end_user_equipment_is_dishwasher(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a Dishwasher?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 1.'


    def formula(buildings, period, parameters):
        equipment_type = buildings('ESS__SONA_equipment_type', period)
        possible_equipment_type = equipment_type.possible_values
        is_dishwasher = (equipment_type == possible_equipment_type.dishwasher)
        return is_dishwasher


class ESS__SONA_end_user_equipment_has_registered_place_settings(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the End User Equipment have a registered number of place settings?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 1.'


class ESS__SONA_dishwasher_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet all of the Equipment' \
            ' Requirements detailed in Activity Definition B3?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3.'

    def formula(buildings, period, parameters):
        is_dishwasher = buildings('ESS__SONA_end_user_equipment_is_dishwasher', period)
        has_registered_place_settings = buildings('ESS__SONA_end_user_equipment_has_registered_place_settings', period)
        is_labelled_for_energy_labelling = buildings('ESS__SONA_equipment_labelled_for_energy_labelling', period)
        return (is_dishwasher *
                has_registered_place_settings *
                is_labelled_for_energy_labelling)
