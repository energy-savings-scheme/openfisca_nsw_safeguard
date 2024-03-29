from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_showerheads_replace_is_installed_by_licensed_plumber(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'The replacement of the showerhead must be performed or supervised' \
            ' by a Licensed plumber in accordance with the' \
            ' Plumbing Code of Australia.'


class ESS_HEER_showerheads_replace_only_one_showerhead_is_replaced(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'A maximum of one showerhead per shower can be replaced, as' \
            ' prescribed by Implementation Requirement 2.'


class ESS_HEER_showerheads_replace_showerhead_is_compatible_with_heating_system(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the showerhead is compatible with the installed' \
            ' water heating system.'


class ESS_HEER_showerheads_replace_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the Implementation meets the Implementation Requirements' \
            ' in Activity Definition E6.'

    def formula(buildings, period, parameters):
        installed_by_licensed_plumber = buildings(
        'ESS_HEER_showerheads_replace_is_installed_by_licensed_plumber', period)
        only_one_showerhead_replaced = buildings(
        'ESS_HEER_showerheads_replace_only_one_showerhead_is_replaced', period)
        is_compatible_with_heating_system = buildings(
        'ESS_HEER_showerheads_replace_showerhead_is_compatible_with_heating_system', period)
