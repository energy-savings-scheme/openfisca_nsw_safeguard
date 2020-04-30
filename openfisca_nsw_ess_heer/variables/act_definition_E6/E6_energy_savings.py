# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E6_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        hot_water_supply_service = buildings('hot_water_supply_service', period)
        HotWaterSupplyService = hot_water_supply_service.possible_values  # imports functionality of hot water supply service types from E6_energy_savings
        water_supply_service = select([(hot_water_supply_service == HotWaterSupplyService.electric_resistance_water_heater),
                (hot_water_supply_service == HotWaterSupplyService.electric_boosted_solar_water_heater),
                (hot_water_supply_service == HotWaterSupplyService.electric_heat_pump_water_heater)],
                ['electric_resistance_water_heater',
                'electric_boosted_solar_water_heater',
                'electric_heat_pump_water_heater'])
        electricity_savings_factor = parameters(period).table_E6_1.electricity_savings_factor[water_supply_service]
        return electricity_savings_factor


class E6_gas_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        hot_water_supply_service = buildings('hot_water_supply_service', period)
        HotWaterSupplyService = hot_water_supply_service.possible_values  # imports functionality of hot water supply service types from E6_energy_savings
        water_supply_service = select([(hot_water_supply_service == HotWaterSupplyService.gas_fired_storage_water_heater),
                (hot_water_supply_service == HotWaterSupplyService.gas_fired_instantaneous_water_heater),
                (hot_water_supply_service == HotWaterSupplyService.gas_boosted_solar_water_heater)],
                ['gas_fired_storage_water_heater',
                'gas_fired_instantaneous_water_heater',
                'gas_boosted_solar_water_heater'])
        electricity_savings_factor = parameters(period).table_E6_2.gas_savings_factor[water_supply_service]
        return electricity_savings_factor
