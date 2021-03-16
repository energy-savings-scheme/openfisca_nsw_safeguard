# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E12_deemed_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    default_value = 0.91
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        energy_savings = 0.91
        return energy_savings
