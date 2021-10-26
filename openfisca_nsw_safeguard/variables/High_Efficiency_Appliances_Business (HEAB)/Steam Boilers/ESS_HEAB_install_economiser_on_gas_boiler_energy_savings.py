from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np



class ESS_HEAB_install_economiser_on_gas_boiler_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F12?'

    def formula(buildings, period, parameters):
        current_capacity = buildings('ESS_HEAB_steam_boiler_current_equipment_capacity', period)
        existing_equipment_type = buildings('ESS_HEAB_steam_boiler_existing_equipment_type', period)
        default_efficiency_improvement = parameters(period).ESS.HEAB.table_F12_1.default_efficiency_improvement[existing_equipment_type]
        load_utilisation_factor = parameters(period).ESS.HEAB.table_F12_2.load_utilisation_factor
        lifetime = parameters(period).ESS.HEAB.table_F12_3.lifetime
        hours_in_year = parameters(period).ESS.ESS_related_constants.hours_in_year
        return (
                current_capacity * 
                default_efficiency_improvement * 
                load_utilisation_factor * 
                lifetime * 
                hours_in_year / 
                1000
                )
        # need to make the burner replacement age calc more efficient