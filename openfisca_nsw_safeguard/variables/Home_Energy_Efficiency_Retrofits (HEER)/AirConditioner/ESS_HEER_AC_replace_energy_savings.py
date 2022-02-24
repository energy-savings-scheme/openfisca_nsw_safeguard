from email.mime import base
import numpy as np
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_core.variables import Variable
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021


class ESS_HEER_AC_replace_electricity_savings(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What are the electricity savings created by replacing an existing AC?'
    metadata = {
        'alias': "HEER AC Replace Electricity Savings",
    }

    def formula(buildings, period, parameters):
        reference_cooling_annual_energy_use = buildings(
            'ESS_HEER_AC_replace_reference_cooling_annual_energy_use', period)
        cooling_annual_energy_use = buildings(
            'ESS_HEER_AC_replace_cooling_annual_energy_use', period)
        reference_heating_annual_energy_use = buildings(
            'ESS_HEER_AC_replace_reference_heating_annual_energy_use', period)
        heating_annual_energy_use = buildings(
            'ESS_HEER_AC_replace_heating_annual_energy_use', period)
        lifetime = (parameters(period).ESS.HEER.table_D16_6.lifetime)
        return(
                (
                    (
                        reference_cooling_annual_energy_use -
                        cooling_annual_energy_use
                    ) +
                    (
                        reference_heating_annual_energy_use -
                        heating_annual_energy_use
                    )
                ) *
            lifetime / 
            1000
                )




class ESS_HEER_AC_replace_reference_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the reference cooling annual energy use for the new AC?'
    metadata = {
        'alias': "HEER AC Cooling Annual Energy Use",
    }

    def formula(buildings, period, parameters):
        AC_cooling_capacity = buildings('new_AC_cooling_capacity', period)
        cooling_capacity = np.select(
            [
                (AC_cooling_capacity < 4),
                    (
                    (AC_cooling_capacity >= 4) * (AC_cooling_capacity < 10)
                    ),
                    (
                    (AC_cooling_capacity >= 10) * (AC_cooling_capacity < 39)
                    ),
                    (
                    (AC_cooling_capacity >= 39) * (AC_cooling_capacity <= 65)
                    ),
                (AC_cooling_capacity > 65)
            ],
            [
                'less_than_4kW',
                '4kW_to_10kW',
                '10kW_to_39kW',
                '39kW_to_65kW',
                'more_than_65kW'
            ]
        )
        product_type = buildings('Air_Conditioner_type', period)
        climate_zone = buildings('AC_climate_zone', period)
        equivalent_cooling_hours = (
            parameters(period).ESS.HEER.table_D16_1['equivalent_cooling_hours'][climate_zone])
        baseline_cooling_AEER = (
            parameters(period).ESS.HEER.table_D16_3['AEER'][product_type][cooling_capacity])
        return(
            (
                AC_cooling_capacity *
                equivalent_cooling_hours) /
                baseline_cooling_AEER
                )


class ESS_HEER_AC_replace_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the cooling annual energy use for the new AC?'
    metadata = {
        'alias': "HEER AC Cooling Annual Energy Use",
    }

    def formula(buildings, period, parameters):
        AC_cooling_capacity = buildings('new_AC_cooling_capacity', period)
        climate_zone = buildings('AC_climate_zone', period)
        equivalent_cooling_hours = (
            parameters(period).ESS.HEER.table_D16_1['equivalent_cooling_hours'][climate_zone])
        rated_AEER = buildings('AC_AEER', period)
        return(
            (
            AC_cooling_capacity *
            equivalent_cooling_hours) /
            rated_AEER
                )


class ESS_HEER_AC_replace_reference_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the reference heating annual energy use for the new AC?'
    metadata = {
        'alias': "HEER AC Cooling Annual Energy Use",
    }

    def formula(buildings, period, parameters):
        AC_heating_capacity = buildings('new_AC_heating_capacity', period)
        heating_capacity = np.select(
            [
                (AC_heating_capacity < 4),
                    (
                    (AC_heating_capacity >= 4) * (AC_heating_capacity < 10)
                    ),
                    (
                    (AC_heating_capacity >= 10) * (AC_heating_capacity < 39)
                    ),
                    (
                    (AC_heating_capacity >= 39) * (AC_heating_capacity <= 65)
                    ),
                (AC_heating_capacity > 65)
            ],
            [
                'less_than_4kW',
                '4kW_to_10kW',
                '10kW_to_39kW',
                '39kW_to_65kW',
                'more_than_65kW'
            ]
        )
        product_type = buildings('Air_Conditioner_type', period)
        climate_zone = buildings('AC_climate_zone', period)
        equivalent_heating_hours = (
            parameters(period).ESS.HEER.table_D16_1['equivalent_heating_hours'][climate_zone])
        baseline_heating_ACOP = (
            parameters(period).ESS.HEER.table_D16_3['ACOP'][product_type][heating_capacity])
        return(
            (
                AC_heating_capacity *
                equivalent_heating_hours) /
                baseline_heating_ACOP
                )


class ESS_HEER_AC_replace_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the heating annual energy use for the new AC?'
    metadata = {
        'alias': "HEER AC Heating Annual Energy Use",
    }

    def formula(buildings, period, parameters):
        AC_heating_capacity = buildings('new_AC_heating_capacity', period)
        climate_zone = buildings('AC_climate_zone', period)
        equivalent_heating_hours = (
            parameters(period).ESS.HEER.table_D16_1['equivalent_heating_hours'][climate_zone])
        rated_ACOP = buildings('AC_ACOP', period)
        return(
            (
            AC_heating_capacity *
            equivalent_heating_hours) /
            rated_ACOP
                )