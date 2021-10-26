# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
import time
import numpy as np
import datetime

# note because this activity definition requires calculation based off years, \
# you need to import the above libraries to make it work

epoch = time.gmtime(0).tm_year
today_date_and_time = np.datetime64(datetime.datetime.now())
today = today_date_and_time.astype('datetime64[D]')

# variables used to calculate age of equipment.


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_replacement_end_user_equipment_is_gas_fired_burner(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the replacement end user equipment a gas fired burner?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_replacement_is_linkageless(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the replacement end user equipment of the linkagless type, as' \
            ' in a two service or stepper motor type?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_replacement_has_minimum_4_1_turn_down_ratio(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the replacement equipment have a turn-down ratio of at least' \
            ' 4:1?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_replacement_can_receive_flue_gas_sensor_signal(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Can the replacement End User Equipment receive a signal from a' \
            ' flue glass sensor, for oxygen trim purposes?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F7?'

    def formula(buildings, period, parameters):
        is_gas_fired_burner = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_replacement_end_user_equipment_is_gas_fired_burner', period)
        replacement_nameplate_capacity = buildings('ESS_HEAB_steam_boiler_current_equipment_capacity', period)
        condition_over_1000kW = (replacement_nameplate_capacity > 1000)
        is_linkageless = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_replacement_is_linkageless', period)
        has_4_1_turndown_ratio = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_replacement_has_minimum_4_1_turn_down_ratio', period)
        can_receive_gas_sensor_signal = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_replacement_can_receive_flue_gas_sensor_signal', period)
        return where(condition_over_1000kW,
                    (is_gas_fired_burner * is_linkageless * has_4_1_turndown_ratio * can_receive_gas_sensor_signal),
                     is_gas_fired_burner)
