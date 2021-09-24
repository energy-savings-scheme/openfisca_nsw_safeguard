from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_showerheads_replace_with_low_flow_showerhead_uses_eligible_hot_water_service(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the hot water service supplying the shower eligible for the activity?'  # this light type is not defined anywhere in the rule (and probably should be!)

    def formula(buildings, period, parameters):
        hot_water_supply_service = buildings('ESS_HEER_hot_water_supply_service', period)
        is_electric_resistance = (hot_water_supply_service == HotWaterSupplyService.electric_resistance_water_heater)
        is_electric_boosted_solar = (hot_water_supply_service == HotWaterSupplyService.electric_boosted_solar_water_heater)
        is_electric_heat_pump = (hot_water_supply_service == HotWaterSupplyService.electric_heat_pump_water_heater)
        is_gas_fired_storage = (hot_water_supply_service == HotWaterSupplyService.gas_fired_storage_water_heater)
        is_gas_fired_instantaneous = (hot_water_supply_service == HotWaterSupplyService.gas_fired_instantaneous_water_heater)
        is_gas_boosted_solar = (hot_water_supply_service == HotWaterSupplyService.gas_boosted_solar_water_heater)
        return is_electric_resistance + is_electric_boosted_solar + is_electric_heat_pump + is_gas_fired_storage + is_gas_fired_instantaneous + is_gas_boosted_solar  # note addition is used to define "or" with booleans


class ESS_HEER_showerheads_replace_with_low_flow_showerhead_has_existing_showerhead(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the shower has an existing showerhead, as required' \
            ' in Eligibility Requirement 3 in Activity Definition E6.'  # insert definition requirements


class HotWaterSupplyService(Enum):
    electric_resistance_water_heater = 'An electric resistance water heater.'
    electric_boosted_solar_water_heater = 'An electrically boosted solar water heater.'
    electric_heat_pump_water_heater = 'An electric heat pump water heater.'
    gas_fired_storage_water_heater = 'A gas fired storage water heater.'
    gas_fired_instantaneous_water_heater = 'A gas fired instantaneous water heater.'
    gas_boosted_solar_water_heater = 'A gas boosted solar water heater.'


class ESS_HEER_hot_water_supply_service(Variable):
    value_type = Enum
    possible_values = HotWaterSupplyService
    default_value = HotWaterSupplyService.electric_resistance_water_heater
    entity = Building
    definition_period = ETERNITY
    label = 'Defines the type of hot water supply service used to supply a' \
            ' a replacement showerhead in Activity Definition E6.'
