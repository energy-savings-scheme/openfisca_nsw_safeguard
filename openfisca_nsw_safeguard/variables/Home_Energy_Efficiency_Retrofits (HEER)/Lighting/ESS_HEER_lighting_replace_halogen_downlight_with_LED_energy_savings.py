from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_HEER_lighting_replace_halogen_downlight_with_LED_residential_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('ESS_HEER_lighting_existing_lamp_type', period)
        new_lamp_type = buildings('ESS_HEER_lighting_new_lamp_type', period)
        new_lamp_circuit_power = buildings('ESS_HEER_lighting_new_lamp_circuit_power', period)
        lamp_rating_power = np.select([new_lamp_circuit_power <= 5,
        ((new_lamp_circuit_power > 5) * (new_lamp_circuit_power <= 10)),
        ((new_lamp_circuit_power > 10) * (new_lamp_circuit_power <= 15)),
        new_lamp_circuit_power > 15],
        ["under_or_equal_to_five_watts",
        "under_or_equal_to_ten_watts",
        "under_or_equal_to_fifteen_watts",
        "over_fifteen_watts"])
        residential_building_savings_factor = (parameters(period).
        ESS.HEER.table_E1_1.residential_savings_factor
        [existing_lamp_type][new_lamp_type][lamp_rating_power])
        return residential_building_savings_factor


class ESS_HEER_lighting_replace_halogen_downlight_with_LED_small_business_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('ESS_HEER_lighting_existing_lamp_type', period)
        new_lamp_type = buildings('ESS_HEER_lighting_new_lamp_type', period)
        new_lamp_circuit_power = buildings('ESS_HEER_lighting_new_lamp_circuit_power', period)
        lamp_rating_power = np.select([new_lamp_circuit_power <= 5,
        ((new_lamp_circuit_power > 5) * (new_lamp_circuit_power <= 10)),
        ((new_lamp_circuit_power > 10) * (new_lamp_circuit_power <= 15)),
        new_lamp_circuit_power > 15],
        ["under_or_equal_to_five_watts",
        "under_or_equal_to_ten_watts",
        "under_or_equal_to_fifteen_watts",
        "over_fifteen_watts"])
        small_business_building_savings_factor = (parameters(period).
        ESS.HEER.table_E1_2.small_business_savings_factor
        [existing_lamp_type][new_lamp_type][lamp_rating_power])
        return small_business_building_savings_factor
