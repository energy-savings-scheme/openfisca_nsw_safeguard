from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class D18_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        Baseline_A = buildings('D18_Baseline_A', period)
        a = 2.355
        Bs = buildings('D18_Bs', period)
        Be = buildings('D18_Be', period)

        electricity_savings = Baseline_A - (a * (Bs + Be))
        return electricity_savings


class D18_System_Size(Enum):
    system_size_small = 'small'
    system_size_medium = 'medium'


class D18_annual_energy_savings(Variable):
    value_type = float  
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        system_size = buildings('D18_system_size', period)
        system_size_int = np.select(
            [
                (system_size == D18_System_Size.system_size_small),
                (system_size == D18_System_Size.system_size_medium)
            ],
            [
                'small',
                'medium'
            ])

        #Baseline A
        Baseline_A = parameters(period).ESS.HEER.table_D18_1['baseline_energy_consumption'][system_size_int]

        #Deemed electricity savings
        a = 2.355
        Bs = buildings('D18_Bs', period)
        Be = buildings('D18_Be', period)

        annual_savings = Baseline_A - (a * (Bs + Be)) 
        return annual_savings


class D18_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        deemed_activity_electricity_savings = buildings('D18_deemed_activity_electricity_savings', period)
        regional_network_factor = buildings('D18_regional_network_factor', period)

        electricity_savings = deemed_activity_electricity_savings * regional_network_factor
        return electricity_savings


class D18_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'output',
        'label' : 'The number of ESCs for D18'
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('D18_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        replacement_activity = buildings('D18_replacement_activity', period)

        D18_eligible_ESCs = np.select(
            [
                replacement_activity,
                np.logical_not(replacement_activity)
            ],
            [
                (electricity_savings * electricity_certificate_conversion_factor),
                0
            ])

        result_to_return = np.select(
            [
                D18_eligible_ESCs <= 0, D18_eligible_ESCs > 0
            ],
            [
                0, D18_eligible_ESCs
            ])
        return result_to_return
