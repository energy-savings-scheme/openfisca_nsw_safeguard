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
        existing_lamp_type = buildings('existing_lamp_type', period)
        new_lamp_type = buildings('new_lamp_type', period)
        new_lamp_circuit_power = buildings('new_lamp_circuit_power', period)
        lamp_rating_power = select([new_lamp_circuit_power <= 5,
        new_lamp_circuit_power > 5 and new_lamp_circuit_power <= 10,
        new_lamp_circuit_power > 10 and new_lamp_circuit_power <= 15],
        ["under_or_equal_to_five_watts",
        "under_or_equal_to_ten_watts",
        "under_or_equal_to_fifteen_watts"])
        residential_building_savings_factor = (parameters(period).energy_savings_scheme.HEER.table_E1_1.residential_savings_factor
        [existing_lamp_type][new_lamp_type][lamp_rating_power])
        return residential_building_savings_factor


class E2_small_business_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('existing_lamp_type', period)
        new_lamp_type = buildings('new_lamp_type', period)
        new_lamp_circuit_power = buildings('new_lamp_circuit_power', period)
        lamp_rating_power = select([new_lamp_circuit_power <= 5,
        new_lamp_circuit_power > 5 and new_lamp_circuit_power <= 10,
        new_lamp_circuit_power > 10 and new_lamp_circuit_power <= 15],
        ["under_or_equal_to_five_watts",
        "under_or_equal_to_ten_watts",
        "under_or_equal_to_fifteen_watts"])
        residential_building_savings_factor = (parameters(period).energy_savings_scheme.HEER.table_E1_2.small_business_savings_factor
        [existing_lamp_type][new_lamp_type][lamp_rating_power])
        return residential_building_savings_factor
