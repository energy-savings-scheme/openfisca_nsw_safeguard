# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEAB_install_sensor_based_blowdown_on_gas_boiler_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F13?'

    def formula(buildings, period, parameters):
        installed_on_single_gas_fired_steam_boiler = buildings('ESS_HEAB_new_equipment_installed_on_single_boiler', period)
        installed_on_multiple_gas_fired_steam_boilers = buildings('ESS_HEAB_new_equipment_installed_on_multiple_boiler', period)
        is_not_residential = buildings('ESS_is_not_residential_building', period)
        replaces_existing_equipment = buildings('ESS_HEAB_steam_boiler_replaces_existing_equipment', period)
        return (
                (
                        installed_on_single_gas_fired_steam_boiler + 
                        installed_on_multiple_gas_fired_steam_boilers
                ) * 
                is_not_residential * 
                (not(replaces_existing_equipment))
                )
