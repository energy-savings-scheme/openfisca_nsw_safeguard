# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEAB_install_motor_to_provide_cooling_motor_is_installed_into_refrigerated_cabinet(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the motor been installed into a refrigerated cabinet?'


class ESS_HEAB_install_motor_to_provide_cooling_motor_is_installed_into_reach_in_freezer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the motor been installed into a reach in freezer?'


class ESS_HEAB_install_motor_to_provide_cooling_motor_is_installed_into_cold_room_evaporator_in_use(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the motor been installed into a cold room evaporator unit,' \
            ' which is in use?'


class ESS_HEAB_install_motor_to_provide_cooling_unit_in_RC_freezer_or_cold_room(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the motor been installed into a refrigerated cabinet, reach in' \
            ' freezer, or a cold room evaporator unit which is in use?'

    def formula(buildings, period, parameters):
        installed_in_RC = buildings('ESS_HEAB_install_motor_to_provide_cooling_motor_is_installed_into_refrigerated_cabinet', period)
        installed_in_reach_in_freezer = buildings('ESS_HEAB_install_motor_to_provide_cooling_motor_is_installed_into_reach_in_freezer', period)
        installed_in_cold_room = buildings('ESS_HEAB_install_motor_to_provide_cooling_motor_is_installed_into_cold_room_evaporator_in_use', period)
        return (installed_in_RC + installed_in_reach_in_freezer + installed_in_cold_room)


class ESS_HEAB_install_motor_to_provide_cooling_unit_replaces_equivalent_shaded_pole_motor_unit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment replace an equivalent shaded pole' \
            ' motor unit?'


class ESS_HEAB_install_motor_to_provide_cooling_unit_replaces_permanent_split_capacitor_motor(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment replace a permanent split' \
            ' capacitor motor?'


class ESS_HEAB_install_motor_to_provide_cooling_replaces_equivalent_shaded_or_permanent_split_unit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment replace an equivalent shaded pole' \
            ' or a permanent split capacitor motor?'

    def formula(buildings, period, parameters):
        replaces_shaded_pole_motor_unit = buildings('ESS_HEAB_install_motor_to_provide_cooling_unit_replaces_equivalent_shaded_pole_motor_unit', period)
        replaces_permanent_split_capacitor_motor = buildings('ESS_HEAB_install_motor_to_provide_cooling_unit_replaces_permanent_split_capacitor_motor', period)
        return (replaces_shaded_pole_motor_unit + replaces_permanent_split_capacitor_motor)


class ESS_HEAB_install_motor_to_provide_cooling_unit_installed_to_manufacturer_guidelines(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the unit been installed according to manufacturer guidelines?'


class ESS_HEAB_install_motor_to_provide_cooling_unit_installed_to_administrator_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the unit been installed according to any additional' \
            ' requirements set out by the Scheme Administrator?'


class ESS_HEAB_install_motor_to_provide_cooling_meets_installation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the installation meet the installation guidelines defined in' \
            ' Activity Definition F5?'

    def formula(buildings, period, parameters):
        installed_in_RC_freezer_or_cold_room = buildings('ESS_HEAB_install_motor_to_provide_cooling_unit_in_RC_freezer_or_cold_room', period)
        replaces_shaded_or_split_unit = buildings('ESS_HEAB_install_motor_to_provide_cooling_replaces_equivalent_shaded_or_permanent_split_unit', period)
        installed_according_to_manufacturer_guidelines = buildings('ESS_HEAB_install_motor_to_provide_cooling_unit_installed_to_administrator_requirements', period)
        installed_according_to_administrator_requirements = buildings('ESS_HEAB_install_motor_to_provide_cooling_unit_installed_to_administrator_requirements', period)
        return (
                installed_in_RC_freezer_or_cold_room * 
                replaces_shaded_or_split_unit * 
                installed_according_to_manufacturer_guidelines * 
                installed_according_to_administrator_requirements
                )
