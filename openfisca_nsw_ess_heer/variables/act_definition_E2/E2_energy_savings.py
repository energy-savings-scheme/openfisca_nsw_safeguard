# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E2_residential_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        existing_lamp_LCP = buildings('existing_lamp_LCP', period)
        LCP_of_existing_lamp = select([existing_lamp_LCP >= 100 and existing_lamp_LCP < 150,
        existing_lamp_LCP >= 150 and existing_lamp_LCP < 200,
        existing_lamp_LCP >= 200 and existing_lamp_LCP < 300,
        existing_lamp_LCP >= 300 and existing_lamp_LCP < 500,
        existing_lamp_LCP >= 500]
        ["existing_lamp_LCP_between_100W_and_150W",
        "existing_lamp_LCP_between_150W_and_200W",
        "existing_lamp_LCP_between_200W_and_300W"
        "existing_lamp_LCP_between_300W_and_500W",
        "existing_lamp_LCP_more_than_500W"])
        new_lamp_type = buildings('new_lamp_type', period)
        new_lamp_circuit_power = buildings('new_lamp_circuit_power', period)
        lamp_rating_power = select([new_lamp_circuit_power <= 30,
        new_lamp_circuit_power > 30 and new_lamp_circuit_power <= 45,
        new_lamp_circuit_power > 45 and new_lamp_circuit_power <= 60,
        new_lamp_circuit_power > 60 and new_lamp_circuit_power <= 90,
        new_lamp_circuit_power > 90 and new_lamp_circuit_power <= 150],
        ["under_30W",
        "more_than_30W_and_less_than_or_equal_to_45W"
        "more_than_45W_and_less_than_or_equal_to_60W"
        "more_than_60W_and_less_than_or_equal_to_90W"
        "more_than_90W_and_less_than_or_equal_to_150W"])
        residential_building_savings_factor = (parameters(period).table_E2_1.residential_savings_factor
        [LCP_of_existing_lamp][new_lamp_type][lamp_rating_power])
        return residential_building_savings_factor


class E2_small_business_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        existing_lamp_LCP = buildings('existing_lamp_LCP', period)
        LCP_of_existing_lamp = select([existing_lamp_LCP >= 100 and existing_lamp_LCP < 150,
        existing_lamp_LCP >= 150 and existing_lamp_LCP < 200,
        existing_lamp_LCP >= 200 and existing_lamp_LCP < 300,
        existing_lamp_LCP >= 300 and existing_lamp_LCP < 500,
        existing_lamp_LCP >= 500],
        ["existing_lamp_LCP_between_100W_and_150W",
        "existing_lamp_LCP_between_150W_and_200W",
        "existing_lamp_LCP_between_200W_and_300W"
        "existing_lamp_LCP_between_300W_and_500W",
        "existing_lamp_LCP_more_than_500W"])
        new_lamp_type = buildings('new_lamp_type', period)
        new_lamp_circuit_power = buildings('new_lamp_circuit_power', period)
        lamp_rating_power = select([new_lamp_circuit_power <= 30,
        new_lamp_circuit_power > 30 and new_lamp_circuit_power <= 45,
        new_lamp_circuit_power > 45 and new_lamp_circuit_power <= 60,
        new_lamp_circuit_power > 60 and new_lamp_circuit_power <= 90,
        new_lamp_circuit_power > 90 and new_lamp_circuit_power <= 150],
        ["under_30W",
        "more_than_30W_and_less_than_or_equal_to_45W"
        "more_than_45W_and_less_than_or_equal_to_60W"
        "more_than_60W_and_less_than_or_equal_to_90W"
        "more_than_90W_and_less_than_or_equal_to_150W"])
        small_business_building_savings_factor = (parameters(period).table_E2_2.small_business_savings_factor
        [LCP_of_existing_lamp][new_lamp_type][lamp_rating_power])
        return small_business_building_savings_factor
