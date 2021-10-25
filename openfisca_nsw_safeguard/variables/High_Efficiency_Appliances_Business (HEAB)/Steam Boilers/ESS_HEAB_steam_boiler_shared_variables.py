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
