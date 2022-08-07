# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_existing_end_user_equipment_is_disconnected_and_removed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the existing End User Equipment been disconnected and removed?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_disconnection_and_removal_performed_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the disconnection and removal of the existing End User' \
            ' Equipment been performed by a qualified person, in accordance' \
            ' with relevant standards and legislation?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_disconnection_and_removal_supervised_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the disconnection and removal of the existing End User' \
            ' Equipment been supervised by a qualified person, in accordance' \
            ' with relevant standards and legislation?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_installed_in_accordance_with_manufacturer_guidelines(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with manufacturer guidelines?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_installed_in_accordance_with_relevant_standards_and_legislation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with relevant standards' \
            ' and legislation?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_installed_in_accordance_with_scheme_administrator_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with other Scheme' \
            ' Administrator Requirements?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F11?'

    def formula(buildings, period, parameters):
        existing_end_equipment_is_disconnected_and_removed = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_existing_end_user_equipment_is_disconnected_and_removed', period)
        disconnection_and_removed_performed_by_qualified_person = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_disconnection_and_removal_performed_by_qualified_person', period)
        disconnection_and_removed_supervised_by_qualified_person = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_disconnection_and_removal_supervised_by_qualified_person', period)
        adheres_to_manufacturers_guidelines = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_installed_in_accordance_with_manufacturer_guidelines', period)
        adheres_to_relevants_standards_and_legislation = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_installed_in_accordance_with_relevant_standards_and_legislation', period)
        adheres_to_scheme_administrator_requirements = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_installed_in_accordance_with_scheme_administrator_requirements', period)
        return ((existing_end_equipment_is_disconnected_and_removed
                * (disconnection_and_removed_performed_by_qualified_person
                + disconnection_and_removed_supervised_by_qualified_person))
                * (adheres_to_manufacturers_guidelines * adheres_to_relevants_standards_and_legislation
                * adheres_to_scheme_administrator_requirements))
