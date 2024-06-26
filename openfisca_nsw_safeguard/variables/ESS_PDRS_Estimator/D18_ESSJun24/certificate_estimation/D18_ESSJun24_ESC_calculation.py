from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class D18_ESSJun24_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        Baseline_A = buildings('D18_ESSJun24_Baseline_A', period)
        a = 2.310
        Bs = buildings('D18_ESSJun24_Bs', period)
        Be = buildings('D18_ESSJun24_Be', period)

        #if Bs and Be values from the registry are 0, calculate 0 savings
        electricity_savings = np.select(
        [
            (Bs <= 0) * (Be <= 0),
            (Bs > 0) * (Be <= 0),
            (Bs > 0) * (Be > 0),
            (Bs <= 0) * (Be > 0)
        ],
        [
            0,
            Baseline_A - (a * (Bs + Be)),
            Baseline_A - (a * (Bs + Be)),
            Baseline_A - (a * (Bs + Be))
        ])
        return electricity_savings


class D18_ESSJun24_System_Size(Enum):
    system_size_small = 'small'
    system_size_medium = 'medium'


class D18_ESSJun24_annual_energy_savings(Variable):
    value_type = float  
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        system_size = buildings('D18_ESSJun24_system_size', period)
        system_size_int = np.select(
            [
                (system_size == D18_ESSJun24_System_Size.system_size_small),
                (system_size == D18_ESSJun24_System_Size.system_size_medium)
            ],
            [
                'small',
                'medium'
            ])

        #Baseline A
        Baseline_A = parameters(period).ESS.HEER.table_D18_1_ESSJun24['baseline_energy_consumption'][system_size_int]

        #Deemed electricity savings
        a = 2.310
        Bs = buildings('D18_ESSJun24_Bs', period)
        Be = buildings('D18_ESSJun24_Be', period)

        deemed_activity_electricity_savings = Baseline_A - (a * (Bs + Be)) 
    
        #regional network factor
        postcode = buildings('D18_ESSJun24_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        regional_network_factor = rnf.calc(postcode)

        #electricity savings
        annual_energy_savings = deemed_activity_electricity_savings * regional_network_factor
    
        annual_savings_return = np.select([
                annual_energy_savings <= 0, annual_energy_savings > 0
            ],
            [
                0, annual_energy_savings
            ])
        
        return annual_savings_return


class D18_ESSJun24_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        deemed_activity_electricity_savings = buildings('D18_ESSJun24_deemed_activity_electricity_savings', period)
        regional_network_factor = buildings('D18_ESSJun24_regional_network_factor', period)

        electricity_savings = deemed_activity_electricity_savings * regional_network_factor
        return electricity_savings


class D18_ESSJun24_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'output',
        'label' : 'The number of ESCs for D18_ESSJun24'
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('D18_ESSJun24_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        replacement_activity = buildings('D18_ESSJun24_replacement_activity', period)

        D18_ESSJun24_eligible_ESCs = np.select(
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
                D18_ESSJun24_eligible_ESCs <= 0, D18_ESSJun24_eligible_ESCs > 0
            ],
            [
                0, D18_ESSJun24_eligible_ESCs
            ])
        return result_to_return
