# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_has_digital_burner_control_system(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment have a digital burner control system installed?'


class ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_digital_burner_control_system_will_be_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Will a digital burner control system be installed?'


class ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F10?'

    def formula(buildings, period, parameters):
        existing_heater_equipment_type = buildings('ESS_HEAB_existing_heater_equipment_type', period)
        HeaterEquipmentType = (existing_heater_equipment_type.possible_values)
        is_gas_fired_steam_boiler = (existing_heater_equipment_type == HeaterEquipmentType.gas_fired_steam_boiler)
        is_hot_water_boiler = (existing_heater_equipment_type == HeaterEquipmentType.hot_water_boiler)
        is_water_heater = (existing_heater_equipment_type == HeaterEquipmentType.water_heater)
        is_not_residential = buildings('ESS_is_not_residential_building', period)
        replaces_existing_end_user_equipment = buildings('ESS_HEAB_steam_boiler_replaces_existing_equipment', period)
        has_digital_burner_control_system = buildings('ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_has_digital_burner_control_system', period)
        digital_burner_control_system_will_be_installed = buildings('ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_digital_burner_control_system_will_be_installed', period)
        return ((is_gas_fired_steam_boiler + is_hot_water_boiler + is_water_heater) * is_not_residential
                * (not(replaces_existing_end_user_equipment))
                * (has_digital_burner_control_system + digital_burner_control_system_will_be_installed))
