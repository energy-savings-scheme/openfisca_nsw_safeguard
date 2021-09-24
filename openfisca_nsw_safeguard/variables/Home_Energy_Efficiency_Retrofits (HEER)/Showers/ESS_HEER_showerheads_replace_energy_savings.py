from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_HEER_showerheads_replace_with_low_flow_showerhead_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the residential electricity savings factor for Activity Definition E6.'

    def formula(buildings, period, parameters):
        hot_water_supply_service = buildings('ESS_HEER_hot_water_supply_service', period)
        HotWaterSupplyService = hot_water_supply_service.possible_values  # imports functionality of hot water supply service types from E6_energy_savings
        water_supply_service = np.select(
                                         [
                                         (hot_water_supply_service == HotWaterSupplyService.electric_resistance_water_heater),
                                         (hot_water_supply_service == HotWaterSupplyService.electric_boosted_solar_water_heater),
                                         (hot_water_supply_service == HotWaterSupplyService.electric_heat_pump_water_heater),
                                         (hot_water_supply_service == HotWaterSupplyService.gas_fired_storage_water_heater),
                                         (hot_water_supply_service == HotWaterSupplyService.gas_fired_instantaneous_water_heater),
                                         (hot_water_supply_service == HotWaterSupplyService.gas_boosted_solar_water_heater)
                                         ],
                                        [
                                        'electric_resistance_water_heater',
                                        'electric_boosted_solar_water_heater',
                                        'electric_heat_pump_water_heater',
                                        'gas_fired_storage_water_heater',
                                        'gas_fired_instantaneous_water_heater',
                                        'gas_boosted_solar_water_heater'
                                        ]
                                        )
        electricity_savings_factor = (parameters(period).
        ESS.HEER.table_E6_1.electricity_savings_factor[water_supply_service])
        return electricity_savings_factor


class ESS_HEER_showerheads_replace_with_low_flow_showerhead_gas_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        hot_water_supply_service = buildings('ESS_HEER_hot_water_supply_service', period)
        HotWaterSupplyService = hot_water_supply_service.possible_values  # imports functionality of hot water supply service types from E6_energy_savings
        water_supply_service = np.select(
                                         [
                                         (hot_water_supply_service == HotWaterSupplyService.electric_resistance_water_heater),
                                         (hot_water_supply_service == HotWaterSupplyService.electric_boosted_solar_water_heater),
                                         (hot_water_supply_service == HotWaterSupplyService.electric_heat_pump_water_heater),
                                         (hot_water_supply_service == HotWaterSupplyService.gas_fired_storage_water_heater),
                                         (hot_water_supply_service == HotWaterSupplyService.gas_fired_instantaneous_water_heater),
                                         (hot_water_supply_service == HotWaterSupplyService.gas_boosted_solar_water_heater),
                                         ],
                                        [
                                        'electric_resistance_water_heater',
                                        'electric_boosted_solar_water_heater',
                                        'electric_heat_pump_water_heater',
                                        'gas_fired_storage_water_heater',
                                        'gas_fired_instantaneous_water_heater',
                                        'gas_boosted_solar_water_heater'
                                        ]
                                        )
        gas_savings_factor = (parameters(period).
        ESS.HEER.table_E6_2.gas_savings_factor[water_supply_service])
        return gas_savings_factor
