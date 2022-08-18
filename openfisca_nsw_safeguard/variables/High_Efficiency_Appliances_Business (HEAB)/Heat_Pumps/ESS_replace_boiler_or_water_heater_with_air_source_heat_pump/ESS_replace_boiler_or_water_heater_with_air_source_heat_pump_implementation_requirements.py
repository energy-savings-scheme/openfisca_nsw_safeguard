from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_existing_hot_water_pump_is_removed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the existing end user equipment been removed?'
    metadata = {
        'alias':  'The existing hot water pump has been removed'
    }

class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the replacement end-user equipment been installed?'
    metadata = {
        'alias':  'The replacement hot water pump is installed'
    }


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End-User equipment meet the Implementation Requirements?'
    metadata = {
        'alias':  'The new end-user equipment meets the implementation requirements'
    }

    def formula(buildings, period, parameters):  
        Existing_hot_water_pump_removed = buildings('ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_existing_hot_water_pump_is_removed', period)
        Replacement_hot_water_pump_equipment_installed = buildings('ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_is_installed', period)
        Installed_or_removed_by_certified = buildings('implementation_is_performed_by_qualified_person', period)

        return (
                Existing_hot_water_pump_removed *
                Replacement_hot_water_pump_equipment_installed *
                Installed_or_removed_by_certified
                )