from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_lighting_replace_PAR_lamp_residential_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        existing_lamp_LCP = buildings('ESS_HEER_lighting_existing_lamp_circuit_power', period)
        LCP_of_existing_lamp = np.select(
                                        [existing_lamp_LCP < 80,
                                         ((existing_lamp_LCP >= 80) * (existing_lamp_LCP < 100)),
                                         ((existing_lamp_LCP >= 100) * (existing_lamp_LCP < 120)),
                                         ((existing_lamp_LCP >= 120) * (existing_lamp_LCP < 140)),
                                         ((existing_lamp_LCP >= 140) * (existing_lamp_LCP < 160)),
                                         (existing_lamp_LCP >= 160)
                                        ],
                                        [
                                        "existing_LCP_less_than_80W",
                                        "existing_LCP_80_to_100W",
                                        "existing_LCP_100_to_120W",
                                        "existing_LCP_120_to_140W",
                                        "existing_LCP_140_to_160W",
                                        "existing_LCP_160W_or_more",
                                        ]
                                        )
        new_EUE_light_output = buildings('ESS_HEER_lighting_new_lamp_light_output', period)
        light_output = np.select([
                                  new_EUE_light_output < 1200,
                                  ((new_EUE_light_output >= 1200) * (new_EUE_light_output <= 1500)),
                                  ((new_EUE_light_output >= 1500) * (new_EUE_light_output <= 1900)),
                                  ((new_EUE_light_output >= 1900) * (new_EUE_light_output <= 2300)),
                                  new_EUE_light_output >= 2300],
                                  [
                                  "less_than_1200_lm",
                                  "between_1200_and_1500_lm",
                                  "between_1500_and_1900_lm",
                                  "between_1900_and_2300_lm",
                                  "more_than_2300_lm"
                                  ]
                                  )
        new_lamp_circuit_power = buildings('ESS_HEER_lighting_new_lamp_circuit_power', period)
        lamp_rating_power = np.select([
                                       new_lamp_circuit_power <= 15,
                                       ((new_lamp_circuit_power > 15) * (new_lamp_circuit_power <= 25)),
                                       ((new_lamp_circuit_power > 25) * (new_lamp_circuit_power <= 30)),
                                       ((new_lamp_circuit_power > 30) * (new_lamp_circuit_power <= 40)),
                                       new_lamp_circuit_power > 40
                                       ],
                                       [
                                       "less_than_15W",
                                       "15W_to_25W",
                                       "25W_to_30W",
                                       "30W_to_40W",
                                       "over_40W"
                                    ]
                                )
        residential_building_savings_factor = (parameters(period).
        ESS.HEER.table_E3_1.residential_savings_factor
        [LCP_of_existing_lamp][light_output][lamp_rating_power])
        return residential_building_savings_factor


class ESS_HEER_lighting_replace_PAR_lamp_small_business_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        existing_lamp_LCP = buildings('ESS_HEER_lighting_existing_lamp_circuit_power', period)
        LCP_of_existing_lamp = np.select(
                                        [existing_lamp_LCP < 80,
                                         ((existing_lamp_LCP >= 80) * (existing_lamp_LCP < 100)),
                                         ((existing_lamp_LCP >= 100) * (existing_lamp_LCP < 120)),
                                         ((existing_lamp_LCP >= 120) * (existing_lamp_LCP < 140)),
                                         ((existing_lamp_LCP >= 140) * (existing_lamp_LCP < 160)),
                                         (existing_lamp_LCP >= 160)
                                        ],
                                        [
                                        "existing_LCP_less_than_80W",
                                        "existing_LCP_80_to_100W",
                                        "existing_LCP_100_to_120W",
                                        "existing_LCP_120_to_140W",
                                        "existing_LCP_140_to_160W",
                                        "existing_LCP_160W_or_more",
                                        ]
                                        )
        new_EUE_light_output = buildings('ESS_HEER_lighting_new_lamp_light_output', period)
        light_output = np.select([
                                  new_EUE_light_output < 1200,
                                  ((new_EUE_light_output >= 1200) * (new_EUE_light_output <= 1500)),
                                  ((new_EUE_light_output >= 1500) * (new_EUE_light_output <= 1900)),
                                  ((new_EUE_light_output >= 1900) * (new_EUE_light_output <= 2300)),
                                  new_EUE_light_output >= 2300],
                                  [
                                  "less_than_1200_lm",
                                  "between_1200_and_1500_lm",
                                  "between_1500_and_1900_lm",
                                  "between_1900_and_2300_lm",
                                  "more_than_2300_lm"
                                  ]
                                  )
        new_lamp_circuit_power = buildings('ESS_HEER_lighting_new_lamp_circuit_power', period)
        lamp_rating_power = np.select([
                                       new_lamp_circuit_power <= 15,
                                       ((new_lamp_circuit_power > 15) * (new_lamp_circuit_power <= 25)),
                                       ((new_lamp_circuit_power > 25) * (new_lamp_circuit_power <= 30)),
                                       ((new_lamp_circuit_power > 30) * (new_lamp_circuit_power <= 40)),
                                       new_lamp_circuit_power > 40
                                       ],
                                       [
                                       "less_than_15W",
                                       "15W_to_25W",
                                       "25W_to_30W",
                                       "30W_to_40W",
                                       "over_40W"
                                    ]
                                )
        small_business_savings_factor = (parameters(period).
        ESS.HEER.table_E3_2.small_business_savings_factor
        [LCP_of_existing_lamp][light_output][lamp_rating_power])
        return small_business_savings_factor
