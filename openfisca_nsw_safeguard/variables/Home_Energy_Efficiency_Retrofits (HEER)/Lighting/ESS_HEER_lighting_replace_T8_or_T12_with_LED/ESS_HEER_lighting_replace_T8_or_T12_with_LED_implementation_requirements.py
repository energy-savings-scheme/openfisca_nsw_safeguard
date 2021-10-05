# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEER_lighting_replace_T8_or_T12_with_LED_is_installed_by_authorised_person(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the activity was performed by a person authorised' \
            ' to carry out electrical wiring work, defined under section 14' \
            ' (1) of the Home Building Act 1989.'


class ESS_HEER_lighting_replace_T8_or_T12_with_LED_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the implementation meets the Implementation Requirements' \
            ' detailed in Activity Definition E5.'
