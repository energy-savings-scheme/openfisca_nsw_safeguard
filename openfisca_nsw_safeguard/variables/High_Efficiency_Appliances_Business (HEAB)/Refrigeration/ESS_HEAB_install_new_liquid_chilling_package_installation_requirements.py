# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEAB_install_new_liquid_chilling_package_LCP_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the LCP been installed?'  # note no definition of what installed means


class ESS_HEAB_install_new_liquid_chilling_package_installation_requirements_are_met(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether all of the installation requirements for Activity' \
            ' Definition F2 are met.'

    def formula(buildings, period, parameters):
        LCP_is_installed = buildings('ESS_HEAB_install_new_liquid_chilling_package_LCP_is_installed', period)
        return not(LCP_is_installed)
