from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_install_external_blind_product_applied_externally_to_outside_of_door_or_window(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Product is applied externally to the outside of the door or window.' \
            ' As prescribed by Implementation Requirement 1.'


class ESS_HEER_install_external_blind_installer_complies_with_SafeWorkNSW_installation_standards(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the person performing the activity complies with' \
            ' the relevant installation standards and legislation outlined by' \
            ' SafeWorkNSW, as prescribed by Implementation Requirement 2.'


class ESS_HEER_install_external_blind_product_installed_according_to_instructions(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product has been installed in strict accordance' \
            ' with the manufacturer instructions, as prescribed by' \
            ' Implementation Requirement 3.'


class ESS_HEER_install_external_blind_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the Implementation meets the Implementation Requirements,' \
            ' as detailed in Activity Definition E10.'

    def formula(buildings, period, parameters):
        blind_applied_externally = buildings(
        'ESS_HEER_install_external_blind_product_applied_externally_to_outside_of_door_or_window', period)
        complies_with_SafeWork = buildings(
        'ESS_HEER_install_external_blind_installer_complies_with_SafeWorkNSW_installation_standards', period)
        installed_according_to_instructions = buildings(
        'ESS_HEER_install_external_blind_product_installed_according_to_instructions', period)
        return (
                blind_applied_externally *
                complies_with_SafeWork *
                installed_according_to_instructions
                )
