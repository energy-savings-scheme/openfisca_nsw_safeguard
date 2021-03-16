# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class installer_authorised_for_electricial_wiring_work(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the installer is authorised for conducting' \
            ' electricial wiring work, under section 14 (1) of the Home' \
            ' Building Act, as required by Implementation Requirement 1.'
