from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


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
        installed_in_residential = buildings('is_installed_in_residential_buildings', period)
        return not(installed_in_residential)
