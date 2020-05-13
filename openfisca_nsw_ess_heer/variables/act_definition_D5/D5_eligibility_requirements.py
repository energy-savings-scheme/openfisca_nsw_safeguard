# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

class existing_pool_pump_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is there an existing pool pump installed at the Site, at the time' \
            ' of the replacement activity?'
