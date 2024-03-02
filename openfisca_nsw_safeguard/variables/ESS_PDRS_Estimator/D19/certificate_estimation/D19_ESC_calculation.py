from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class D19_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        Baseline_A = buildings('D19_Baseline_A', period)
        a = 2.320
        Bs = buildings('D19_Bs', period)
        Be = buildings('D19_Be', period)

        electricity_savings = Baseline_A - (a * (Bs + Be))
        return electricity_savings
    

class D19_System_Size(Enum):
    system_size_small = 'small'
    system_size_medium = 'medium'


class D19_annual_energy_savings(Variable):
    value_type = float  
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        #system size
        system_size = buildings('D19_system_size', period)
        system_size_int = np.select(
            [
                (system_size == D19_System_Size.system_size_small),
                (system_size == D19_System_Size.system_size_medium)
            ],
            [
                'small',
                'medium'
            ])
        
        #Baseline A
        Baseline_A = parameters(period).ESS.HEER.table_D19_1['baseline_energy_consumption'][system_size_int]['baseline_A']
        
        #Baseline B (deemed gas savings)
        Baseline_B = parameters(period).ESS.HEER.table_D19_1['baseline_energy_consumption'][system_size_int]['baseline_B']

        #Deemed electricity savings
        a = 2.320
        Bs = buildings('D19_Bs', period)
        Be = buildings('D19_Be', period)

        deemed_electricity_savings = Baseline_A - (a * (Bs + Be))
        deemed_gas_savings = Baseline_B

        #regional network factor
        postcode = buildings('D17_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        regional_network_factor = rnf.calc(postcode)

        #electricity savings
        electricity_savings = deemed_electricity_savings * regional_network_factor
    
        #annual savings
        annual_energy_savings = electricity_savings + deemed_gas_savings


        annual_savings_return = np.select([
                annual_energy_savings <= 0, annual_energy_savings > 0
            ],
            [
                0, annual_energy_savings
            ])
        
        return annual_savings_return
        
        
class D19_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        deemed_activity_electricity_savings = buildings('D19_deemed_activity_electricity_savings', period)
        regional_network_factor = buildings('D19_regional_network_factor', period)

        electricity_savings = deemed_activity_electricity_savings * regional_network_factor
        return electricity_savings


class D19_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'output',
        'label' : 'The number of ESCs for D19'
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('D19_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        gas_savings = buildings('D19_Baseline_B', period)
        gas_certificate_conversion_factor = 0.47
        replacement_activity = buildings('D19_replacement_activity', period)

        D19_eligible_ESCs = np.select(
            [
                replacement_activity,
                np.logical_not(replacement_activity)
            ],
            [
                ((electricity_savings * electricity_certificate_conversion_factor) + (gas_savings * gas_certificate_conversion_factor)),
                0
            ])

        result_to_return = np.select(
            [
                D19_eligible_ESCs <= 0, D19_eligible_ESCs > 0
            ],
            [
                0, D19_eligible_ESCs
            ])
        return result_to_return
