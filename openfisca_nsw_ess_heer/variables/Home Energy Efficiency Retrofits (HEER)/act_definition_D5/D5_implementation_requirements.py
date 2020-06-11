# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class is_installed_by_licensed_plumber_or_electrician(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the pool pump installed by a licensed plumber or electrician?'  # ask if this is required by the standards?
    documentation = 'Variable X'


class is_decommissioned_pool_pump_removed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the decomissioned pool pump removed?'  # what does removed mean
    # in this context? note that we refer specifically to the existing
    # standard for defining what removed means. there's no definition
    # for removed in 9.8 (which governs HEER.)


class is_installed_by_relevant_installer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks if the EUE has been installed by the relevant installer.'


class D4_is_installed_by_relevant_installer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks if the EUE has been installed by the relevant installer.'


class D5_is_installed_by_relevant_installer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks if the EUE has been installed by the relevant installer.'
