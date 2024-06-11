from xml.etree import ElementInclude
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class WH1_F16_electric_PDRSAug24_capacity_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Capacity Factor'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      HP_cap = buildings('WH1_F16_electric_PDRSAug24_HP_capacity_factor', period)
      WH_cap = buildings('WH1_F16_electric_PDRSAug24_WH_capacity_factor', period)

      capacity_factor = np.select(
                                 [
                                    (HP_cap <= WH_cap),
                                    (HP_cap > WH_cap)
                                 ],
                                 [
                                    1,
                                    WH_cap / HP_cap
                                 ]
                                 )

      return capacity_factor
    

class WH1_F16_electric_PDRSAug24_Ref_Elec(Variable):
    """ Annual Electrical Energy used by a reference electric resistance water heater in a year
    """
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Reference electricity'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        com_peak_load = buildings('WH1_F16_electric_PDRSAug24_com_peak_load', period)

        # we divide this by 1000 to convert MJ to GJ
        ref_elec = 365 * 0.905 * 1.05 * (com_peak_load / 1000)
        return ref_elec
    

class WH1_F16_electric_PDRSAug24_deemed_activity_gas_savings(Variable):
    #this is the deemed gas savings for a replacing electric equipment
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      HP_gas = buildings('WH1_F16_electric_PDRSAug24_HP_gas', period)
      capacity_factor = buildings('WH1_F16_electric_PDRSAug24_capacity_factor', period)
      lifetime = parameters(period).ESS.HEAB.table_F16_1.lifetime

      deemed_gas_savings = (-HP_gas) * capacity_factor * (lifetime / 3.6)
      return deemed_gas_savings
    

class WH1_F16_electric_PDRSAug24_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        ref_elec = buildings('WH1_F16_electric_PDRSAug24_Ref_Elec', period)
        HP_elec = buildings('WH1_F16_electric_PDRSAug24_HP_elec', period)
        capacity_factor = buildings('WH1_F16_electric_PDRSAug24_capacity_factor', period)
        lifetime = parameters(period).ESS.HEAB.table_F16_1['lifetime']

        deemed_electricity_savings = (ref_elec - HP_elec) * capacity_factor * (lifetime / 3.6)
        return deemed_electricity_savings    


class WH1_F16_electric_PDRSAug24_energy_savings(Variable):
    value_type = float  
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #ref elec
        com_peak_load = buildings('WH1_F16_electric_PDRSAug24_com_peak_load', period)
        
        ref_elec = 365 * 0.905 * 1.05 * (com_peak_load / 1000)

        #HP elec
        HP_elec = buildings('WH1_F16_electric_PDRSAug24_HP_elec', period)

        #HP gas
        HP_gas = buildings('WH1_F16_electric_PDRSAug24_HP_gas', period)

        #capacity factor
        HP_Cap = buildings('WH1_F16_electric_PDRSAug24_HP_capacity_factor', period)
        WH_Cap = buildings('WH1_F16_electric_PDRSAug24_WH_capacity_factor', period)

        capacity_factor = np.select(
                                 [
                                    (HP_Cap <= WH_Cap),
                                    (HP_Cap > WH_Cap)
                                 ],
                                 [
                                    1,
                                    WH_Cap / HP_Cap
                                 ])
        
        #lifetime
        lifetime = parameters(period).ESS.HEAB.table_F16_1['lifetime']

        #gas savings for replacing electric
        deemed_gas_savings = (-HP_gas) * capacity_factor * (lifetime / 3.6)

        #electricity savings for replacing electric
        deemed_electricity_savings = (ref_elec - HP_elec) * capacity_factor * (lifetime / 3.6)
       
        #annual energy savings
        annual_energy_savings = deemed_electricity_savings + deemed_gas_savings
    
        annual_savings_return = np.select([
            annual_energy_savings <= 0, annual_energy_savings > 0
        ], 
	    [
            0, annual_energy_savings
        ])
        
        return annual_savings_return


class WH1_F16_electric_PDRSAug24_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        deemed_activity_electricity_savings = buildings('WH1_F16_electric_PDRSAug24_deemed_activity_electricity_savings', period)
        regional_network_factor = buildings('WH1_F16_electric_PDRSAug24_regional_network_factor', period)

        electricity_savings = deemed_activity_electricity_savings * regional_network_factor
        return electricity_savings


class WH1_F16_electric_PDRSAug24_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'output',
        'label' : 'The number of ESCs for WH1'
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('WH1_F16_electric_PDRSAug24_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        gas_savings = buildings('WH1_F16_electric_PDRSAug24_deemed_activity_gas_savings', period) #gas savings and deemed activity gas savings are the same value
        gas_certificate_conversion_factor = 0.47
        replacement_activity = buildings('WH1_F16_electric_PDRSAug24_replacement_activity', period)

        WH1_eligible_ESCs = np.select(
            [
                replacement_activity,
                np.logical_not(replacement_activity)
            ],
            [
                (electricity_savings * electricity_certificate_conversion_factor) + (gas_savings * gas_certificate_conversion_factor),
                0
            ])

        result_to_return = np.select(
            [
                WH1_eligible_ESCs <= 0, WH1_eligible_ESCs > 0
            ],
            [
                0, WH1_eligible_ESCs
            ])
        return result_to_return