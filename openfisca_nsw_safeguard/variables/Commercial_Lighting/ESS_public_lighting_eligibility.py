from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY, YEAR
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

import numpy as np
from datetime import date


class ESS_PL_is_eligible_for_public_lighting(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible for the Commercial Lighting method,' \
            ' as detailed in Clause 9.4?'

    def formula(buildings, period, parameters):
        is_eligible_activity_type = buildings('ESS_CL_is_eligible_activity_type', period)


class ESS_PL_is_eligible_activity_type(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Commercial Lighting an eligible activity type?'

    def formula(buildings, period, parameters):
        is_lighting_for_roads_and_public_spaces = (
            buildings('ESS_CL_is_lighting_for_roads_and_public_spaces', period))
        is_lighting_for_traffic_signals = (
            buildings('ESS_CL_is_traffic_signals', period))
        is_building_lighting = (
            buildings('ESS_CL_is_building_lighting', period))


class ESS_PL_is_lighting_for_roads_and_public_spaces(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a lighting upgrade for Roads and Public Spaces?'


class ESS_PL_is_traffic_signals(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a lighting upgrade for Traffic Lighting?'


class ESS_PL_is_building_lighting(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a lighting upgrade for Building Lighting?'