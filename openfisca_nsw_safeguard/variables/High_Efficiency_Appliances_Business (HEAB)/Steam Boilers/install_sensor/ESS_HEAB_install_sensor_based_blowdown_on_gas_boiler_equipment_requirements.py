from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np



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
