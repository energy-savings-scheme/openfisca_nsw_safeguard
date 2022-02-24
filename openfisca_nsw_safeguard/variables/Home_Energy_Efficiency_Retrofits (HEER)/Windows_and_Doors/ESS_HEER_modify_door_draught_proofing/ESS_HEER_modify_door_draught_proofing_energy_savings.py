from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_modify_external_door_draught_proofing_residential_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the Residential Electricity Savings Factor for Activity Definition E7.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('ESS_HEER_new_product_warranty_length', period)
        warranty_period = np.select(
                                    [
                                     warranty_length < 2,
                                     ((warranty_length >= 2) * (warranty_length <= 5)),
                                     warranty_length > 5
                                     ],
                                     [
                                      "less_than_two_year_warranty",
                                      "two_to_five_year_warranty",
                                      "over_five_year_warranty"
                                      ]
                                      )
        climate_zone = buildings('BCA_climate_zone', period)
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
        residential_electricity_savings_factor = (
        parameters(period).ESS.HEER.table_E7_1.residential_electricity_savings_factor[warranty_period][activity_climate_zone])
        return residential_electricity_savings_factor


class ESS_HEER_modify_external_door_draught_proofing_residential_gas_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the Residential Electricity Savings Factor for Activity Definition E7.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('ESS_HEER_new_product_warranty_length', period)
        warranty_period = np.select(
                                    [
                                     warranty_length < 2,
                                     ((warranty_length >= 2) * (warranty_length <= 5)),
                                     warranty_length > 5
                                     ],
                                     [
                                      "less_than_two_year_warranty",
                                      "two_to_five_year_warranty",
                                      "over_five_year_warranty"
                                      ]
                                      )
        climate_zone = buildings('BCA_climate_zone', period)
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
        ESS.HEER.table_E7_2.residential_gas_savings_factor[warranty_period][activity_climate_zone])
        return residential_gas_savings_factor


class ESS_HEER_modify_external_door_draught_proofing_small_business_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('ESS_HEER_new_product_warranty_length', period)
        warranty_period = np.select(
                                    [
                                     warranty_length < 2,
                                     ((warranty_length >= 2) * (warranty_length <= 5)),
                                     warranty_length > 5
                                     ],
                                     [
                                      "less_than_two_year_warranty",
                                      "two_to_five_year_warranty",
                                      "over_five_year_warranty"
                                      ]
                                      )
        climate_zone = buildings('BCA_climate_zone', period)
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
        ESS.HEER.table_E7_3.small_business_electricity_savings_factor[warranty_period][activity_climate_zone])
        return small_business_electricity_savings_factor


class ESS_HEER_modify_external_door_draught_proofing_small_business_gas_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('ESS_HEER_new_product_warranty_length', period)
        warranty_period = np.select(
                                    [
                                     warranty_length < 2,
                                     ((warranty_length >= 2) * (warranty_length <= 5)),
                                     warranty_length > 5
                                     ],
                                     [
                                      "less_than_two_year_warranty",
                                      "two_to_five_year_warranty",
                                      "over_five_year_warranty"
                                      ]
                                      )
        climate_zone = buildings('BCA_climate_zone', period)
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
        ESS.HEER.table_E7_4.small_business_gas_savings_factor[warranty_period][activity_climate_zone])
        return small_business_gas_savings_factor
