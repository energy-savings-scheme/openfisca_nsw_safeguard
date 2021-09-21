# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

import numpy as np

class ESS_HEER_windows_modify_residential_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the residential electricity savings factor for the' \
            ' thermally efficient window or door.'

    def formula(buildings, period, parameters):
        window_or_door_rating = buildings('ESS_HEER_window_or_door_U_value', period)
        U_value_rating = np.select([
                                    window_or_door_rating >= 3,
                                    ((window_or_door_rating >= 2) * (window_or_door_rating < 3)),
                                    ((window_or_door_rating >= 1 ) * (window_or_door_rating < 2)),
                                    window_or_door_rating < 1
                                    ],
                                    [
                                    "system_U_value_over_3",
                                    "system_U_value_over_2",
                                    "system_U_value_over_1",
                                    "system_U_value_under_1"
                                    ]
                                    )
        climate_zone = buildings('ESS__BCA_climate_zone', period)
        BCAClimateZone = climate_zone.possible_values  # imports functionality of climate zone enum from user_inputs
        activity_climate_zone = np.select([
                                        (climate_zone == BCAClimateZone.BCA_Climate_Zone_1),
                                        ((climate_zone == BCAClimateZone.BCA_Climate_Zone_2) + (climate_zone == BCAClimateZone.BCA_Climate_Zone_3)),
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_4,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_5,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_6,
                                        ((climate_zone == BCAClimateZone.BCA_Climate_Zone_7) + (climate_zone == BCAClimateZone.BCA_Climate_Zone_8))
                                        ],
                                       [
                                        "climate_zone_1",
                                        "climate_zones_2_and_3",
                                        "climate_zone_4",
                                        "climate_zone_5",
                                        "climate_zone_6",
                                        "climate_zones_7_and_8"
                                        ]
                                        )
        residential_electricity_savings_factor = (parameters(period).
        ESS.HEER.table_D2_2.residential_electricity_savings_factor[U_value_rating][activity_climate_zone])
        return residential_electricity_savings_factor


class ESS_HEER_windows_modify_residential_gas_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the residential gas savings factor for the' \
            ' thermally efficient window or door.'

    def formula(buildings, period, parameters):
        window_or_door_rating = buildings('ESS_HEER_window_or_door_U_value', period)
        U_value_rating = np.select([
                                    window_or_door_rating >= 3,
                                    ((window_or_door_rating >= 2) * (window_or_door_rating < 3)),
                                    ((window_or_door_rating >= 1 ) * (window_or_door_rating < 2)),
                                    window_or_door_rating < 1
                                    ],
                                    [
                                    "system_U_value_over_3",
                                    "system_U_value_over_2",
                                    "system_U_value_over_1",
                                    "system_U_value_under_1"
                                    ]
                                    )
        climate_zone = buildings('ESS__BCA_climate_zone', period)
        BCAClimateZone = climate_zone.possible_values  # imports functionality of climate zone enum from user_inputs
        activity_climate_zone = np.select([
                                        (climate_zone == BCAClimateZone.BCA_Climate_Zone_1),
                                        ((climate_zone == BCAClimateZone.BCA_Climate_Zone_2) + (climate_zone == BCAClimateZone.BCA_Climate_Zone_3)),
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_4,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_5,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_6,
                                        ((climate_zone == BCAClimateZone.BCA_Climate_Zone_7) + (climate_zone == BCAClimateZone.BCA_Climate_Zone_8))
                                        ],
                                       [
                                        "climate_zone_1",
                                        "climate_zones_2_and_3",
                                        "climate_zone_4",
                                        "climate_zone_5",
                                        "climate_zone_6",
                                        "climate_zones_7_and_8"
                                        ]
                                        )
        residential_gas_savings_factor = (parameters(period).
        ESS.HEER.table_D2_3.residential_gas_savings_factor[U_value_rating][activity_climate_zone])
        return residential_gas_savings_factor


class ESS_HEER_windows_modify_small_business_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the residential electricity savings factor for the' \
            ' thermally efficient window or door.'

    def formula(buildings, period, parameters):
        window_or_door_rating = buildings('ESS_HEER_window_or_door_U_value', period)
        U_value_rating = np.select([
                                    window_or_door_rating >= 3,
                                    ((window_or_door_rating >= 2) * (window_or_door_rating < 3)),
                                    ((window_or_door_rating >= 1 ) * (window_or_door_rating < 2)),
                                    window_or_door_rating < 1
                                    ],
                                    [
                                    "system_U_value_over_3",
                                    "system_U_value_over_2",
                                    "system_U_value_over_1",
                                    "system_U_value_under_1"
                                    ]
                                    )
        climate_zone = buildings('ESS__BCA_climate_zone', period)
        BCAClimateZone = climate_zone.possible_values  # imports functionality of climate zone enum from user_inputs
        activity_climate_zone = np.select([
                                        (climate_zone == BCAClimateZone.BCA_Climate_Zone_1),
                                        ((climate_zone == BCAClimateZone.BCA_Climate_Zone_2) + (climate_zone == BCAClimateZone.BCA_Climate_Zone_3)),
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_4,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_5,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_6,
                                        ((climate_zone == BCAClimateZone.BCA_Climate_Zone_7) + (climate_zone == BCAClimateZone.BCA_Climate_Zone_8))
                                        ],
                                       [
                                        "climate_zone_1",
                                        "climate_zones_2_and_3",
                                        "climate_zone_4",
                                        "climate_zone_5",
                                        "climate_zone_6",
                                        "climate_zones_7_and_8"
                                        ]
                                        )
        small_business_electricity_savings_factor = (parameters(period).
        ESS.HEER.table_D2_4.small_business_electricity_savings_factor[U_value_rating][activity_climate_zone])
        return small_business_electricity_savings_factor


class ESS_HEER_windows_modify_small_business_gas_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the residential gas savings factor for the' \
            ' thermally efficient window or door.'

    def formula(buildings, period, parameters):
        window_or_door_rating = buildings('ESS_HEER_window_or_door_U_value', period)
        U_value_rating = np.select([
                                    window_or_door_rating >= 3,
                                    ((window_or_door_rating >= 2) * (window_or_door_rating < 3)),
                                    ((window_or_door_rating >= 1 ) * (window_or_door_rating < 2)),
                                    window_or_door_rating < 1
                                    ],
                                    [
                                    "system_U_value_over_3",
                                    "system_U_value_over_2",
                                    "system_U_value_over_1",
                                    "system_U_value_under_1"
                                    ]
                                    )
        climate_zone = buildings('ESS__BCA_climate_zone', period)
        BCAClimateZone = climate_zone.possible_values  # imports functionality of climate zone enum from user_inputs
        activity_climate_zone = np.select([
                                        (climate_zone == BCAClimateZone.BCA_Climate_Zone_1),
                                        ((climate_zone == BCAClimateZone.BCA_Climate_Zone_2) + (climate_zone == BCAClimateZone.BCA_Climate_Zone_3)),
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_4,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_5,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_6,
                                        ((climate_zone == BCAClimateZone.BCA_Climate_Zone_7) + (climate_zone == BCAClimateZone.BCA_Climate_Zone_8))
                                        ],
                                       [
                                        "climate_zone_1",
                                        "climate_zones_2_and_3",
                                        "climate_zone_4",
                                        "climate_zone_5",
                                        "climate_zone_6",
                                        "climate_zones_7_and_8"
                                        ]
                                        )
        small_business_gas_savings_factor = (parameters(period).
        ESS.HEER.table_D2_5.small_business_gas_savings_factor[U_value_rating][activity_climate_zone])
        return small_business_gas_savings_factor
