from openfisca_core.entities import entity
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

import numpy as np

class AC_TCSPF_or_AEER_exceeds_ESS_benchmark(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Air Conditioner have a Residential TCSPF mixed equal or greater than the minimum' \
            ' TCSPF mixed listed in Table D16.3? If the TCPSF is not available, is the Rated' \
            ' AEER equal or greater than the Minimum Rated AEER listed in Table D16.5?'
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
            (AC_AEER >= parameters(period).PDRS.AC.table_D16_5[product_class][cooling_capacity]),
            (AC_TCSPF >= parameters(period).PDRS.AC.table_D16_4[product_class][cooling_capacity])
            )
        return AC_exceeds_benchmark


class AC_HSPF_or_ACOP_exceeds_ESS_benchmark(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Air Conditioner have a Residential HSPF mixed equal or greater than the minimum' \
            ' HSPF mixed listed in Table D16.3? If the HSPF is not available, is the Rated' \
            ' ACOP equal or greater than the Minimum Rated ACOP listed in Table D16.5?'
    metadata = {
        'alias':  'ESS - HSPF or ACOP exceeds benchmark',
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        AC_HSPF_mixed = buildings('AC_HSPF_mixed', period)
        AC_HSPF_cold = buildings('AC_HSPF_cold', period)
        AC_ACOP = buildings('AC_ACOP', period)

        product_class = buildings('Air_Conditioner_type', period)
        AC_Class = (product_class.possible_values)

        new_AC_heating_capacity = buildings('new_AC_heating_capacity', period)
        heating_capacity = np.select(
                                    [
                                        (new_AC_heating_capacity < 4),
                                        ((new_AC_heating_capacity >= 4) * (new_AC_heating_capacity < 6)),
                                        ((new_AC_heating_capacity >= 6) * (new_AC_heating_capacity < 10)),
                                        ((new_AC_heating_capacity >= 10) * (new_AC_heating_capacity < 13)),
                                        ((new_AC_heating_capacity >= 13) * (new_AC_heating_capacity < 25)),
                                        ((new_AC_heating_capacity >= 25) * (new_AC_heating_capacity <= 65)),
                                        (new_AC_heating_capacity > 65)
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

        climate_zone = buildings('AC_climate_zone', period)
        ACClimateZone = climate_zone.possible_values
        in_cold_zone = (climate_zone == ACClimateZone.cold_zone)

        AC_HSPF = np.where(
                            in_cold_zone,
                            AC_HSPF_cold,
                            AC_HSPF_mixed)
        # determines which HSPF value to use
        HSPF_is_zero = (
                        (AC_HSPF == 0) + 
                        (AC_HSPF == None)
                        )
        # tells you if the relevant HSPF is zero or non-existant
        AC_exceeds_benchmark = np.select([
                                            HSPF_is_zero,
                                            np.logical_not(HSPF_is_zero) * in_cold_zone,
                                            np.logical_not(HSPF_is_zero) * np.logical_not(in_cold_zone),
                                            ],
                                            [
            (AC_ACOP >= parameters(period).ESS.HEER.table_D16_5['ACOP'][product_class][heating_capacity]),
            (AC_HSPF >= parameters(period).ESS.HEER.table_D16_4['HSPF_cold'][product_class][heating_capacity]),
            (AC_HSPF >= parameters(period).ESS.HEER.table_D16_4['HSPF_mixed'][product_class][heating_capacity])
                                            ]
            )
        return AC_exceeds_benchmark
