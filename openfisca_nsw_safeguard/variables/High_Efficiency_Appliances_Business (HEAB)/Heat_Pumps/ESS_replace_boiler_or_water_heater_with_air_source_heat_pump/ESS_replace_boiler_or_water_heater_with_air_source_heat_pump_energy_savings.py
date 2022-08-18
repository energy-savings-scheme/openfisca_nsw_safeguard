from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'F16 Gas Savings'
    metadata = {
        'alias':  'The existing hot water pump has been removed'
    }

    def formula(buildings, period, parameters):
        equipment_type = buildings('ESS_replace_boiler_with_heat_pump_existing_equipment_type', period)
        ExistingEquipmentType = equipment_type.possible_values

        reference_electricity_use = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_RefElec', period)
        electricity_use = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_HPElec', period)
        gas_use = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_HPGas', period)

        capacity_factor = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_capacity_factor', period)
        lifetime = parameters(period).ESS.HEAB.table_F16_1.lifetime

        is_gas_equipment = (
                                (equipment_type == ExistingEquipmentType.Gas_Hot_Water_Heater) +
                                (equipment_type == ExistingEquipmentType.Gas_Hot_Water_Boiler)
                            )
        is_electric_equipment = (
                                    (equipment_type == ExistingEquipmentType.Electric_Hot_Water_Heater) +
                                    (equipment_type == ExistingEquipmentType.Electric_Hot_Water_Boiler)                                

        )

        deemed_electricity_savings = np.select(
                                                [
                                                    is_gas_equipment,
                                                    is_electric_equipment,
                                                    np.logical_not(
                                                        is_gas_equipment +
                                                        is_electric_equipment
                                                    )
                                                ],
                                                [                                                    (
                                                        (
                                                            (reference_electricity_use / 0.788) - 
                                                            gas_use) *
                                                        capacity_factor *
                                                        lifetime /
                                                        3.6
                                                    ),
                                                    (
                                                        (- electricity_use) *
                                                        capacity_factor *
                                                        lifetime /
                                                        3.6
                                                    ),
                                                    0
                                                ]
        )
        
        return deemed_electricity_savings



class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'F16 Electricity Savings'
    metadata = {
        'alias':  'The existing hot water pump has been removed'
    }

    def formula(buildings, period, parameters):
        equipment_type = buildings('ESS_replace_boiler_with_heat_pump_existing_equipment_type', period)
        ExistingEquipmentType = equipment_type.possible_values

        reference_electricity_use = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_RefElec', period)
        electricity_use = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_HPElec', period)
        gas_use = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_HPGas', period)

        capacity_factor = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_capacity_factor', period)
        lifetime = parameters(period).ESS.HEAB.table_F16_1.lifetime

        is_gas_equipment = (
                                (equipment_type == ExistingEquipmentType.Gas_Hot_Water_Heater) +
                                (equipment_type == ExistingEquipmentType.Gas_Hot_Water_Boiler)
                            )
        is_electric_equipment = (
                                    (equipment_type == ExistingEquipmentType.Electric_Hot_Water_Heater) +
                                    (equipment_type == ExistingEquipmentType.Electric_Hot_Water_Boiler)                                

        )

        deemed_electricity_savings = np.select(
                                                [
                                                    is_gas_equipment,
                                                    is_electric_equipment,
                                                    np.logical_not(
                                                        is_gas_equipment +
                                                        is_electric_equipment
                                                    )
                                                ],
                                                [
                                                    (
                                                        (- gas_use) *
                                                        capacity_factor *
                                                        lifetime /
                                                        3.6
                                                    ),
                                                    (
                                                        (reference_electricity_use - electricity_use) *
                                                        capacity_factor *
                                                        lifetime /
                                                        3.6
                                                    ),
                                                    0
                                                ]
        )
        
        return deemed_electricity_savings


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_RefElec(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'F16 RefElec'
    metadata = {
        'alias':  'The existing hot water pump has been removed'
    }


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_HPElec(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'F16 RefElec'
    metadata = {
        'alias':  'The existing hot water pump has been removed'
    }


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_HPGas(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'F16 RefElec'
    metadata = {
        'alias':  'The existing hot water pump has been removed'
    }


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_new_equipment_rated_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'F16 RefElec'
    metadata = {
        'alias':  'The existing hot water pump has been removed'
    }


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_existing_equipment_rated_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'F16 RefElec'
    metadata = {
        'alias':  'The existing hot water pump has been removed'
    }


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_capacity_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'F16 RefElec'
    metadata = {
        'alias':  'The existing hot water pump has been removed'
    }

    def formula(buildings, period, parameters):
        new_equipment_capacity = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_new_equipment_rated_capacity', period) 
        existing_equipment_capacity = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_existing_equipment_rated_capacity', period) 

        capacity_factor = np.where(
            existing_equipment_capacity >= new_equipment_capacity,
            1,
            existing_equipment_capacity / new_equipment_capacity
        )

        return capacity_factor