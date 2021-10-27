from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class ESS_HEAB_steam_boiler_current_equipment_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the nameplate capacity for the existing equipment, in kW?'


class ESS_HEAB_existing_end_user_equipment_installed_on_gas_fired_steam_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on a gas fired' \
            ' steam boiler?'


class ESS_HEAB_existing_end_user_equipment_installed_on_hot_water_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on a hot water boiler?'


class ESS_HEAB_existing_end_user_equipment_is_gas_fired_burner(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment a gas fired burner?'


class ESS_HEAB_steam_boiler_new_equipment_operating_pressure(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the type of operating pressure of the boiler, as defined' \
            ' in AS3814, in bars of pressure?'


class ESS_HEAB_new_equipment_installed_on_single_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on a single gas fired' \
            ' steam boiler?'


class ESS_HEAB_new_equipment_installed_on_multiple_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on multiple gas fired' \
            ' steam boilers?'


class ESS_HEAB_steam_boiler_replaces_existing_equipment(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment replace existing End User Equipment?'


class ESS_HEAB_steam_boiler_existing_equipment_has_sensor_based_blowdown_control(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment have a sensor based blowdown control installed' \
            ' at the time of commissioning the End User Equipment?'


class ESS_HEAB_sensor_based_blowdown_control_installed_at_commissioning(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment have a sensor based blowdown control installed' \
            ' at the time of commissioning the End User Equipment?'


class SteamBoilerEquipmentType(Enum):
    steam_boiler = 'Trim system is installed on a steam boiler.'
    hot_water_boiler = 'Trim system is installed on a hot water boiler.'
    water_heater = 'Trim system is installed on a water heater.'
    condensing_steam_boiler = 'Trim system is installed on a condensing steam boiler.'


class ESS_HEAB_install_trim_system_steam_boiler_existing_equipment_type(Variable):
    value_type = Enum
    possible_values = SteamBoilerEquipmentType
    default_value = SteamBoilerEquipmentType.steam_boiler
    entity = Building
    definition_period = ETERNITY
    label = 'What is the type of existing equipment that the trim system is being installed on?'


class HeaterEquipmentType(Enum):
    gas_fired_steam_boiler = 'Existing equipment is a gas fired steam boiler.'
    hot_water_boiler = 'Existing equipment is a hot water boiler.'
    water_heater = 'Existing equipment is a water heater.'


class ESS_HEAB_existing_heater_equipment_type(Variable):
    value_type = Enum
    possible_values = HeaterEquipmentType
    default_value = HeaterEquipmentType.gas_fired_steam_boiler
    entity = Building
    definition_period = ETERNITY
    label = 'What is the type of existing equipment used for heating purposes?'


class ESS_HEAB_steam_boiler_exhaust_temperature(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the exhaust temperature of the End User Equipment, while' \
            ' at high-firing, in degrees C?'
