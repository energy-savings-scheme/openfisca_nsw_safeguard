# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E6_is_installed_by_licensed_plumber(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'The replacement of the showerhead must be performed or supervised' \
            ' by a Licensed plumber in accordance with the' \
            ' Plumbing Code of Australia.'


class only_one_showerhead_is_replaced(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'A maximum of one showerhead per shower can be replaced, as' \
            ' prescribed by Implementation Requirement 2.'


class showerhead_is_compatible_with_heating_system(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the showerhead is compatible with the installed' \
            ' water heating system.'
