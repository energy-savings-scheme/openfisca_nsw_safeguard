# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEAB_install_oxygen_trim_system_on_boiler_or_heater_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F10?'

    def formula(buildings, period, parameters):
        current_capacity = buildings('ESS_HEAB_steam_boiler_current_equipment_capacity', period)
        existing_equipment_type = buildings('ESS_HEAB_existing_heater_equipment_type', period)
        default_efficiency_improvement = parameters(period).ESS.HEAB.table_F10_1.default_efficiency_improvement[existing_equipment_type]
        load_utilisation_factor = parameters(period).ESS.HEAB.table_F10_2.load_utilisation_factor
        lifetime = parameters(period).ESS.HEAB.table_F10_3.lifetime
        hours_in_year = parameters(period).ESS.ESS_related_constants.hours_in_year
        return (
                current_capacity * 
                default_efficiency_improvement * 
                load_utilisation_factor * 
                lifetime * 
                hours_in_year / 
                1000
                )