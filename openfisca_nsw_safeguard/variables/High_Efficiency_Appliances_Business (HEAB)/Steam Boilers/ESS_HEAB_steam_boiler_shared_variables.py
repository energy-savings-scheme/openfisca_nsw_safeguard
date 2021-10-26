# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

class ESS_HEAB_steam_boiler_current_equipment_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the nameplate capacity for the existing equipment, in kW?'


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


