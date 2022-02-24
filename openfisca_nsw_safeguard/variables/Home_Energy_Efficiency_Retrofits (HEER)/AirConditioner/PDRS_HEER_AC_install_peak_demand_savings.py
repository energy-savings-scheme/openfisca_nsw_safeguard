from email.mime import base
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

import numpy as np


class PDRS_HEER_AC_install_peak_demand_savings_capacity(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the peak demand savings capacity created by installing a new AC?'
    metadata = {
        'alias': "HEER AC Install Baseline Input Power",
    }

    def formula(buildings, period, parameters):
        baseline_input_power = buildings('PDRS_HEER_AC_install_baseline_input_power', period)
        baseline_peak_adjustment_factor = buildings('PDRS_HEER_AC_install_baseline_peak_adjustment_factor', period)
        AC_input_power = buildings('AC_input_power', period)
        firmness_factor = parameters(period).PDRS.table_A29_firmness_factor.firmness_factor['HVAC1']
        return(
                (baseline_input_power * baseline_peak_adjustment_factor) -
                (AC_input_power * baseline_peak_adjustment_factor) *
                firmness_factor
            )


class PDRS_HEER_AC_install_baseline_input_power(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the baseline input power created by installing a new AC?'
    metadata = {
        'alias': "HEER AC Install Baseline Input Power",
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
        baseline_EER = (parameters(period).PDRS.AC.table_HVAC_1_1[product_type][cooling_capacity])
        return (AC_cooling_capacity / baseline_EER)


class PDRS_HEER_AC_install_baseline_peak_adjustment_factor(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the baseline peak adjustment factor created by installing a new AC?'
    metadata = {
        'alias': "HEER AC Install Baseline Peak Adjustment Factor",
    }

    def formula(buildings, period, parameters):
        BCA_climate_zone = buildings(
            'BCA_climate_zone', period)
        temperature_factor = parameters(period).PDRS.table_A28_temperature_factor.temperature_factor[BCA_climate_zone]
        usage_factor = 0.72
        return (
            temperature_factor * 
            usage_factor
        )
