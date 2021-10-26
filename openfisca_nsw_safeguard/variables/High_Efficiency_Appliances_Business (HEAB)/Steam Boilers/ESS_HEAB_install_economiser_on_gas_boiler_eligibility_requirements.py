from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np



class ESS_HEAB_install_economiser_on_gas_boiler_existing_end_user_equipment_installed_on_gas_fired_steam_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on a gas fired' \
            ' steam boiler?'


class ESS_HEAB_install_economiser_on_gas_boiler_existing_end_user_equipment_installed_on_hot_water_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on a hot water boiler?'


class ESS_HEAB_install_economiser_on_gas_boiler_existing_end_user_equipment_installed_on_water_heater(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on a water heater?'


class ESS_HEAB_install_economiser_on_gas_boiler_existing_steam_boiler_is_condensing_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing steam boiler a condenser boiler?'


class ESS_HEAB_install_economiser_on_gas_boiler_existing_hot_water_boiler_is_condensing_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing hot water boiler a condenser boiler?'


class ESS_HEAB_install_economiser_on_gas_boiler_existing_water_heater_is_condensing_heater(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing water heater a condenser heater?'


class ESS_HEAB_install_economiser_on_gas_boiler_is_heating_feedwater_stream(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End Use Equipment pre-heating a feedwater stream?'


class ESS_HEAB_install_economiser_on_gas_boiler_has_heat_rejection_stream(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the End User Equipment have a heat rejection stream, available' \
            ' for at least 80% of the operating time of the steam boiler,' \
            ' hot water boiler or water heater?'


class ESS_HEAB_install_economiser_on_gas_boiler_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F12?'

    def formula(buildings, period, parameters):
        installed_on_gas_fired_steam_boiler = buildings('ESS_HEAB_install_economiser_on_gas_boiler_existing_end_user_equipment_installed_on_gas_fired_steam_boiler', period)
        installed_on_water_boiler = buildings('ESS_HEAB_install_economiser_on_gas_boiler_existing_end_user_equipment_installed_on_hot_water_boiler', period)
        installed_on_water_heater = buildings('ESS_HEAB_install_economiser_on_gas_boiler_existing_end_user_equipment_installed_on_water_heater', period)
        is_not_residential = buildings('ESS_is_not_residential_building', period)
        replaces_existing_equipment = buildings('ESS_HEAB_steam_boiler_replaces_existing_equipment', period)
        is_condensing_steam_boiler = buildings('ESS_HEAB_install_economiser_on_gas_boiler_existing_steam_boiler_is_condensing_boiler', period)
        is_condensing_hot_water_boiler = buildings('ESS_HEAB_install_economiser_on_gas_boiler_existing_hot_water_boiler_is_condensing_boiler', period)
        is_condensing_heater = buildings('ESS_HEAB_install_economiser_on_gas_boiler_existing_water_heater_is_condensing_heater', period)
        has_heating_feedwater_stream = buildings('ESS_HEAB_install_economiser_on_gas_boiler_is_heating_feedwater_stream', period)
        has_heat_rejection_stream = buildings('ESS_HEAB_install_economiser_on_gas_boiler_has_heat_rejection_stream', period)
        return ((installed_on_gas_fired_steam_boiler + installed_on_water_boiler + installed_on_water_heater)
                * is_not_residential * (not(replaces_existing_equipment))
                * ((not(is_condensing_steam_boiler)) * (not(is_condensing_hot_water_boiler)) * (not(is_condensing_heater)))
                * (has_heating_feedwater_stream + ((not(has_heating_feedwater_stream)) * has_heat_rejection_stream)))
