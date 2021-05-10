# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class is_installed_in_residential_building(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the AC is installed in a residential building, as' \
            ' prescribed in Installation Requirement 1 of Activity' \
            ' Definition F4.'  # you could also ask them for the building type using an Enum if you want to get more sophisticated


class installation_requirements_are_met(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether all of the installation requirements for Activity' \
            ' Definition F4 are met.'

    def formula(buildings, period, parameters):
        installed_in_residential = buildings(
            'is_installed_in_residential_buildings', period)
        return not(installed_in_residential)
