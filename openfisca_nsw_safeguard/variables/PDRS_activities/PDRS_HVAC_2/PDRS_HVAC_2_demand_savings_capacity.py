
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

import numpy as np

class PDRS_HVAC_2_peak_demand_saving_capacity(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the peak demand capacity created by conducting the HVAC 1 activity?"
    metadata = {
        "alias": "AC Peak Demand Savings"
    }

    def formula(buildings, period, parameters):
        baseline_power_input = buildings(
            'PDRS_AC_baseline_input_power', period)
        baseline_peak_adjustment_factor = buildings(
            'PDRS_AC_baseline_peak_adjustment_factor', period)
        input_power = buildings('PDRS_AC_input_power', period)
        peak_adjustment_factor = baseline_peak_adjustment_factor
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor.firmness_factor['HVAC2']

        return (
                    (
                        baseline_power_input *
                        baseline_peak_adjustment_factor
                    ) -
                    (
                        input_power *
                        peak_adjustment_factor
                    )
                    *
                    firmness_factor
            )


class PDRS_HVAC_2_baseline_input_power(Variable):
    value_type = float
    entity = Building
    label = 'returns the baseline input power for an Air Conditioner'
    definition_period = ETERNITY
    metadata = {
        "alias": "Baseline Power Input",
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        cooling_capacity = buildings(
            'Air_Conditioner__cooling_capacity', period)
        baseline_AEER = buildings(
            'PDRS_HVAC_1_baseline_AEER', period)
        return cooling_capacity / baseline_AEER


class PDRS_HVAC_2_baseline_AEER(Variable):
    value_type = float
    entity = Building
    label = 'returns the baseline input power for an Air Conditioner, for activity HVAC 1'
    definition_period = ETERNITY
    metadata = {
        "alias": "Baseline Power Input",
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        product_class = buildings('Air_Conditioner_type', period)
        installation_type = buildings('Appliance__installation_type', period)
        install_or_replacement = installation_type.possible_values
        new_AC_cooling_capacity = buildings('new_AC_cooling_capacity', period)
        cooling_capacity = np.select(
                                    [ 
                                        new_AC_cooling_capacity < 4,
                                        ((new_AC_cooling_capacity >= 4) * (new_AC_cooling_capacity < 10)),
                                        ((new_AC_cooling_capacity >= 10) * (new_AC_cooling_capacity < 39)),
                                        ((new_AC_cooling_capacity >= 39) * (new_AC_cooling_capacity <= 65)),
                                        (new_AC_cooling_capacity > 65)
                                    ],
                                    [
                                        "less_than_4kW",
                                        "4kW_to_10kW",
                                        "10kW_to_39kW",
                                        "39kW_to_65kW",
                                        "more_than_65kW",
                                    ]
                                    )
        baseline_AEER = np.select([
                                    installation_type == install_or_replacement.install,
                                    installation_type == install_or_replacement.replacement,
                                    ],
                                    [
                                        parameters(period).PDRS.AC.table_HVAC_2_1[product_class][cooling_capacity],
                                        parameters(period).PDRS.AC.table_HVAC_2_2[product_class][cooling_capacity]
                                    ])
        return baseline_AEER


class PDRS_HVAC_2_TCSPF_or_AEER_exceeds_benchmark(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Air Conditioner have a Residential TCSPF mixed equal or greater than the minimum' \
            ' TCSPF mixed listed in Table HVAC 1.3? If the TCPSF is not available, is the Rated' \
            ' AEER equal or greater than the Minimum Rated AEER listed in Table HVAC1.4?'
    metadata = {
        'alias':  'Air Conditioner has at least 5 years of Warranty',
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        AC_TCSPF = buildings('AC_TCSPF_mixed', period)
        AC_AEER = buildings('AC_AEER', period)
        product_class = buildings('Air_Conditioner_type', period)
        AC_Class = (product_class.possible_values)
        new_AC_cooling_capacity = buildings('new_AC_cooling_capacity', period)
        cooling_capacity = np.select(
                                    [
                                        (new_AC_cooling_capacity < 4),
                                        ((new_AC_cooling_capacity >= 4) * (new_AC_cooling_capacity < 6)),
                                        ((new_AC_cooling_capacity >= 6) * (new_AC_cooling_capacity < 10)),
                                        ((new_AC_cooling_capacity >= 10) * (new_AC_cooling_capacity < 13)),
                                        ((new_AC_cooling_capacity >= 13) * (new_AC_cooling_capacity < 25)),
                                        ((new_AC_cooling_capacity >= 25) * (new_AC_cooling_capacity <= 65)),
                                        (new_AC_cooling_capacity > 65)
                                    ],
                                    [
                                        "less_than_4kW",
                                        "4kW_to_6kW",
                                        "6kW_to_10kW",
                                        "10kW_to_13kW",
                                        "13kW_to_25kW",
                                        "25kW_to_65kW",
                                        "over_65kW"
                                    ]
                                    )
        TCSPF_is_zero = ((AC_TCSPF == 0) + (AC_TCSPF == None))
        AC_exceeds_benchmark = np.where(
            TCSPF_is_zero,
            (AC_AEER >= parameters(period).PDRS.AC.table_HVAC_2_4[product_class][cooling_capacity]),
            (AC_TCSPF >= parameters(period).PDRS.AC.table_HVAC_2_3[product_class][cooling_capacity])
            )
        return AC_exceeds_benchmark
