# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E3_residential_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        existing_lamp_LCP = buildings('existing_lamp_LCP', period)
        LCP_of_existing_lamp = select([existing_lamp_LCP >= 80 and existing_lamp_LCP < 100,
        existing_lamp_LCP >= 100 and existing_lamp_LCP < 120,
        existing_lamp_LCP >= 120 and existing_lamp_LCP < 140,
        existing_lamp_LCP >= 140 and existing_lamp_LCP < 160],
        ["existing_LCP_80_to_100W",
        "existing_LCP_100_to_120W",
        "existing_LCP_120_to_140W",
        "existing_LCP_140_to_160W"])
        new_EUE_light_output = buildings('new_lamp_light_output', period)
        light_output = select([new_EUE_light_output >= 1200 and new_EUE_light_output <= 1500,
        new_EUE_light_output >= 1500 and new_EUE_light_output <= 1900,
        new_EUE_light_output >= 1900 and new_EUE_light_output <= 2300,
        new_EUE_light_output >= 2300],
        ["between_1200_and_1500_lm",
        "between_1500_and_1900_lm",
        "between_1900_and_2300_lm",
        "more_than_2300_lm"])
        new_lamp_circuit_power = buildings('new_lamp_circuit_power', period)
        lamp_rating_power = select([new_lamp_circuit_power <= 15,
        new_lamp_circuit_power > 15 and new_lamp_circuit_power <= 25,
        new_lamp_circuit_power > 25 and new_lamp_circuit_power <= 30,
        new_lamp_circuit_power > 30 and new_lamp_circuit_power <= 40],
        ["under_or_equal_to_fifteen_watts",
        "fifteen_to_twenty_five_watts",
        "twenty_five_to_thirty_watts",
        "thirty_to_fourty_watts"])
        residential_building_savings_factor = (parameters(period).table_E3_1.residential_savings_factor
        [LCP_of_existing_lamp][light_output][lamp_rating_power])
        return residential_building_savings_factor


class E3_small_business_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        existing_lamp_LCP = buildings('existing_lamp_LCP', period)
        LCP_of_existing_lamp = select([existing_lamp_LCP >= 80 and existing_lamp_LCP < 100,
        existing_lamp_LCP >= 100 and existing_lamp_LCP < 120,
        existing_lamp_LCP >= 120 and existing_lamp_LCP < 140,
        existing_lamp_LCP >= 140 and existing_lamp_LCP < 160],
        ["existing_LCP_80_to_100W",
        "existing_LCP_100_to_120W",
        "existing_LCP_120_to_140W",
        "existing_LCP_140_to_160W"])
        new_EUE_light_output = buildings('new_lamp_light_output', period)
        light_output = select([new_EUE_light_output >= 1200 and new_EUE_light_output <= 1500,
        new_EUE_light_output >= 1500 and new_EUE_light_output <= 1900,
        new_EUE_light_output >= 1900 and new_EUE_light_output <= 2300,
        new_EUE_light_output >= 2300],
        ["between_1200_and_1500_lm",
        "between_1500_and_1900_lm",
        "between_1900_and_2300_lm",
        "more_than_2300_lm"])
        new_lamp_circuit_power = buildings('new_lamp_circuit_power', period)
        lamp_rating_power = select([new_lamp_circuit_power <= 15,
        new_lamp_circuit_power > 15 and new_lamp_circuit_power <= 25,
        new_lamp_circuit_power > 25 and new_lamp_circuit_power <= 30,
        new_lamp_circuit_power > 30 and new_lamp_circuit_power <= 40],
        ["under_or_equal_to_fifteen_watts",
        "fifteen_to_twenty_five_watts",
        "twenty_five_to_thirty_watts",
        "thirty_to_fourty_watts"])
        small_business_savings_factor = (parameters(period).table_E3_2.small_business_savings_factor
        [LCP_of_existing_lamp][light_output][lamp_rating_power])
        return small_business_savings_factor
