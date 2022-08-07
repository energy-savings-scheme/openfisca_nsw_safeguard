from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F14?'

    def formula(buildings, period, parameters):
        installed_on_single_gas_fired_steam_boiler = buildings('ESS_HEAB_new_equipment_installed_on_single_boiler', period)
        installed_on_multiple_gas_fired_steam_boilers = buildings('ESS_HEAB_new_equipment_installed_on_multiple_boiler', period)
        is_not_residential = buildings('ESS_is_not_residential_building', period)
        replaces_existing_equipment = buildings('ESS_HEAB_steam_boiler_replaces_existing_equipment', period)
        has_existing_blowdown_control = buildings('ESS_HEAB_steam_boiler_existing_equipment_has_sensor_based_blowdown_control', period)
        had_blowdown_at_commissioning = buildings('ESS_HEAB_sensor_based_blowdown_control_installed_at_commissioning', period)
        return ((installed_on_single_gas_fired_steam_boiler + installed_on_multiple_gas_fired_steam_boilers)
               * is_not_residential * (not(replaces_existing_equipment))
               * (has_existing_blowdown_control + had_blowdown_at_commissioning))
