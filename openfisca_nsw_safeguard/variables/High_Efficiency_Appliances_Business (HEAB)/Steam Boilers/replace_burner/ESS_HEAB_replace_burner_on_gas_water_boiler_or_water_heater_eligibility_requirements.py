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


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_existing_end_user_equipment_installed_on_water_heater(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on a water heater?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_existing_equipment_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end use equipment in working order?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_existing_equipment_more_than_10_years_old(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end use equipment more than 10 years old?'

    def formula(buildings, period, parameters):
        existing_equipment_age = buildings('ESS_HEAB_existing_equipment_age', period)
        return (existing_equipment_age > 10)


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_existing_equipment_has_air_fuel_ratio(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the existing End Use Equipment have an air\'fuel ratio that is' \
            ' controlled by a mechanical link?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_existing_equipment_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing End User Equipment in working order?'


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F11?'

    def formula(buildings, period, parameters):
        is_gas_fired_burner = buildings('ESS_HEAB_existing_end_user_equipment_is_gas_fired_burner', period)
        installed_on_gas_fired_steam_boiler = buildings('ESS_HEAB_existing_end_user_equipment_installed_on_gas_fired_steam_boiler', period)
        installed_on_water_boiler = buildings('ESS_HEAB_existing_end_user_equipment_installed_on_hot_water_boiler', period)
        installed_on_water_heater = buildings('ESS_HEAB_existing_end_user_equipment_is_gas_fired_burner', period)
        is_not_residential = np.logical_not(buildings('ESS_PDRS_is_residential', period))
        in_working_order = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_existing_equipment_in_working_order', period)
        more_than_10_years_old = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_existing_equipment_more_than_10_years_old', period)
        has_air_fuel_ratio = buildings('ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_existing_equipment_has_air_fuel_ratio', period)
        return (is_gas_fired_burner * (installed_on_gas_fired_steam_boiler + installed_on_water_boiler + installed_on_water_heater)
                * is_not_residential * in_working_order * more_than_10_years_old * has_air_fuel_ratio)
