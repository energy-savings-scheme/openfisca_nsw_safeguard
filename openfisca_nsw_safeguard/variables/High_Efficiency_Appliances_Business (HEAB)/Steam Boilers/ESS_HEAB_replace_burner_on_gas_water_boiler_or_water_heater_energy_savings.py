# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEAB_replace_burner_on_gas_water_boiler_or_water_heater_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F11?'

    def formula(buildings, period, parameters):
        current_capacity = buildings('ESS_HEAB_steam_boiler_current_equipment_capacity', period)
        default_efficiency_improvement = parameters(period).ESS.HEAB.table_F11_1.default_efficiency_improvement
        load_utilisation_factor = parameters(period).ESS.HEAB.table_F11_2.load_utilisation_factor
        lifetime = parameters(period).ESS.HEAB.table_F11_3.lifetime
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