from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np



class ESS_HEAB_install_close_circuit_AC_electricity_savings(Variable):
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
        baseline = parameters(period).ESS.HEAB.table_F3_1.EER_baseline[capacity]
        EFLH = parameters(period).ESS.HEAB.table_F3_1.EER_baseline[capacity]
        lifetime = parameters(period).ESS.HEAB.table_F3_2
        MWh_conversion = parameters(period).general_ESS.unit_conversion_factors['kWh_to_MWh']
        energy_savings = ((((cooling_capacity / baseline) - (cooling_capacity / EER))
                         * EFLH * lifetime) / MWh_conversion)
        return energy_savings


