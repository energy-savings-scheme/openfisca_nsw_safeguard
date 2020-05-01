# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E11_residential_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        new_lamp_LCP = buildings('new_lamp_circuit_power', period)
        new_lamp_light_output = buildings('new_lamp_light_output', period)
        new_lamp_luminous_efficacy = new_lamp_light_output / new_lamp_LCP
        energy_savings = new_lamp_LCP * (new_lamp_luminous_efficacy / 33.9 - 1) * 840 * 10 / 1000000
        return energy_savings


class E11_small_business_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        new_lamp_LCP = buildings('new_lamp_circuit_power', period)
        new_lamp_light_output = buildings('new_lamp_light_output', period)
        new_lamp_luminous_efficacy = new_lamp_light_output / new_lamp_LCP
        energy_savings = new_lamp_LCP * (new_lamp_luminous_efficacy / 33.9 - 1) * 3000 * 10 / 1000000
        return energy_savings
