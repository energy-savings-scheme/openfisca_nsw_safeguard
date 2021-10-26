# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEAB_install_sensor_based_blowdown_on_gas_boiler_is_capable_of_automatic_blowdown(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment capable of automatically blowing down,' \
            ' based on a sensor reading of the total dissolved solids in the' \
            ' steam boiler?'


class ESS_HEAB_install_sensor_based_blowdown_on_gas_boiler_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F13?'

    def formula(buildings, period, parameters):
        is_sensor_based_blowdown = buildings('ESS_HEAB_steam_boiler_existing_equipment_has_sensor_based_blowdown_control', period)
        capable_of_automatic_blowdown = buildings('ESS_HEAB_install_sensor_based_blowdown_on_gas_boiler_is_capable_of_automatic_blowdown', period)
        return(is_sensor_based_blowdown * capable_of_automatic_blowdown)
