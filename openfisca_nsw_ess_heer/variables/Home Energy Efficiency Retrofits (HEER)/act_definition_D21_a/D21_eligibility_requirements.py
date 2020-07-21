# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

class D21_a_is_gas_storage_heater(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment a gas storage heater?'


class D21_a_is_instantanenous_water_heater(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment an instantaneous water heater?'


class D21_a_is_gas_storage_or_instantanenous_water_heater(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment an electric resistance storage heater' \
            ' or an instantaneous water heater?'

    def formula(buildings, period, parameters):
        is_resistance_heater = buildings('D21_a_is_gas_storage_heater', period)
        is_instantaneous_heater = buildings('D21_a_is_instantanenous_water_heater', period)
        return (is_resistance_heater + is_instantaneous_heater)


class D21_a_meets_all_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the eligibilty requirements for' \
            ' Activity Definition F16 (version A)?'

    def formula(buildings, period, parameters):
        is_gas_storage_or_instantaneous = buildings('D21_a_is_gas_storage_or_instantanenous_water_heater', period)
        return is_gas_storage_or_instantaneous
