# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E4_residential_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        lamp_size = buildings('existing_lamp_length', period)
        size_of_existing_lamp = select([lamp_size == 2, lamp_size == 3, lamp_size == 4, lamp_size == 5],
        ["2_foot",
        "3_foot",
        "4_foot",
        "5_foot"])
        residential_building_savings_factor = (parameters(period).table_E4_1.residential_savings_factor
        [size_of_existing_lamp])
        return residential_building_savings_factor


class E4_small_business_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        lamp_size = buildings('existing_lamp_length', period)
        size_of_existing_lamp = select([lamp_size == 2, lamp_size == 3, lamp_size == 4, lamp_size == 5],
        ["2_foot",
        "3_foot",
        "4_foot",
        "5_foot"])
        small_business_savings_factor = (parameters(period).table_E4_2.small_business_savings_factor
        [size_of_existing_lamp])
        return small_business_savings_factor
