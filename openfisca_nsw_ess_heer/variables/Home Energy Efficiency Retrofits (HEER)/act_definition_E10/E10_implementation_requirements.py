# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class product_applied_externally_to_outside_of_door_or_window(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Product is applied externally to the outside of the door or window.' \
            ' As prescribed by Implementation Requirement 1.'


class installer_complies_with_SafeWorkNSW_installation_standards(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the person performing the activity complies with' \
            ' the relevant installation standards and legislation outlined by' \
            ' SafeWorkNSW, as prescribed by Implementation Requirement 2.'


class E10_product_installed_according_to_instructions(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product has been installed in strict accordance' \
            ' with the manufacturer instructions, as prescribed by' \
            ' Implementation Requirement 3.'
