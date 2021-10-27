# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_end_user_equipment_has_oxygen_trim_system(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the End User Equipment have an oxygen trim system?'
    # this is a good example of something that could be used to test TJ's question \
    # weighting tool. if this is false, there is no need to ask the below questions.


class ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_oxygen_trim_system_has_flue_gas_sensor(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the End User Equipment has an oxygen trim system, does it include' \
            ' a flue gas sensor, connected to a control panel?'


class ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_trim_system_capable_of_controlling_burner_air_supply(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the oxygen trim system capable of sending a signal to a control' \
            ' damper on the burner air supply?'


class ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_trim_system_capable_of_controlling_variable_speed_drive(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the oxygen trim system capable of sending a signal to a variable' \
            ' speed drive on the fan motor?'


class ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F10?'

    def formula(buildings, period, parameters):
        has_oxygen_trim_system = buildings('ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_end_user_equipment_has_oxygen_trim_system', period)
        has_flue_gas_sensor = buildings('ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_oxygen_trim_system_has_flue_gas_sensor', period)
        can_control_burner_air_supply = buildings('ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_trim_system_capable_of_controlling_burner_air_supply', period)
        can_control_variable_speed_drive = buildings('ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_trim_system_capable_of_controlling_variable_speed_drive', period)
        return (has_oxygen_trim_system * has_flue_gas_sensor
        * (can_control_burner_air_supply + can_control_variable_speed_drive))
