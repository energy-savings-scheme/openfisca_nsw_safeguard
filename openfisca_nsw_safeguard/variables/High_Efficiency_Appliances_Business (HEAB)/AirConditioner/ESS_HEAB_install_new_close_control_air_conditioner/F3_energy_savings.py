# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F3_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F3?'

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('new_AC_cooling_capacity', period)
        EER = buildings('new_AC_EER', period) # probably should write EER in full
        capacity = select(
                          [
                                cooling_capacity < 19.05,
                                cooling_capacity >= 19.05 and cooling_capacity < 39.5,
                                cooling_capacity >= 39.5 and cooling_capacity < 70.0,
                                cooling_capacity >= 70.0
                           ],
                          [
                                'less_than_19_05_kW',
                                '19_05_kW_to_39_50_kW',
                                '39_50_kW_to_70_kW',
                                'more_than_70_kW'
                           ]
                         )
        baseline = parameters(period).HEAB.F3.F3_1[capacity]
        EFLH = parameters(period).HEAB.F3.hours
        lifetime = parameters(period).HEAB.F3.lifetime
        MWh_conversion = parameters(period).general_ESS.unit_conversion_factors['kWh_to_MWh']
        energy_savings = ((((cooling_capacity / baseline) - (cooling_capacity / EER))
                         * EFLH * lifetime) / MWh_conversion)
        return energy_savings


class F3_CCAC_cooling_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the cooling capacity for the new close control air' \
            ' conditioner, as determined by AS4965.1?'


class F3_EER(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the EER for the new close control air conditioner, as' \
            ' determined by AS4965.1?'
