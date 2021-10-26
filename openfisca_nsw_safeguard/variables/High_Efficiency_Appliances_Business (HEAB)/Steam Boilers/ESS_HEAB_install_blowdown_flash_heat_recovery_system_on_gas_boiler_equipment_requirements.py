# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_end_user_equipment_is_blowdown_flash_steam_heat_recovery_system(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed a blowdown flash steam heat recovery system?'


class ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_injects_flash_steam_from_blowdown_to_feed_water(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the End User Equipment inject flash steam from boiler blowdown' \
            ' into a boiler feed water tank?'


class ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_uses_sub_surface_sparge_line(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the End User Equipment use a sub-surface sparge line to inject '\
            ' flash steam?'


class ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F14?'

    def formula(buildings, period, parameters):
        is_blowdown_system = buildings('ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_end_user_equipment_is_blowdown_flash_steam_heat_recovery_system', period)
        injects_flash_steam = buildings('ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_injects_flash_steam_from_blowdown_to_feed_water', period)
        uses_sub_surface_sparge_line = buildings('ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_uses_sub_surface_sparge_line', period)
        return(is_blowdown_system * injects_flash_steam * uses_sub_surface_sparge_line)
