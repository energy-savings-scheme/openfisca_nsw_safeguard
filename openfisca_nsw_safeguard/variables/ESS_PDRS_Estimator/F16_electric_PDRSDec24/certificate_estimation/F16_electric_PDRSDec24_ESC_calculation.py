from xml.etree import ElementInclude
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class F16_electric_PDRSDec24_PDRS__postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata={
        'variable-type' : 'user-input',
        'alias' : 'ESS Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1,
        'label': 'Postcode'
    }


class F16_electric_PDRSDec24_capacity_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Capacity Factor'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      HP_cap = buildings('F16_electric_PDRSDec24_HP_capacity_factor', period)
      WH_cap = buildings('F16_electric_PDRSDec24_WH_capacity_factor', period)

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
    

class F16_electric_PDRSDec24_individual_heat_pump_thermal_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Individual Heat Pump Thermal Capacity (kW)'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        total_heat_pump_thermal_capacity = buildings('F16_electric_PDRSDec24_total_heat_pump_thermal_capacity', period)
        number_of_heat_pumps = buildings('F16_electric_PDRSDec24_number_of_heat_pumps', period)
        individual_heat_pump_thermal_capacity = total_heat_pump_thermal_capacity / number_of_heat_pumps

        return individual_heat_pump_thermal_capacity
    

class F16_electric_PDRSDec24_confidence_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Confidence Factor'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        """
        Confidence Factor value is calculated as follows:
        if individual heat pump thermal capacity greater than or equal to 10 then confidence_factor value is 1
        otherwise check the value of calculated com peak load
        if the calculated com peak load value is greater than or equal to 1 then confidence_factor value is 1
        otherwise use calculated com peak load value
        """
        individual_heat_pump_thermal_capacity = buildings('F16_electric_PDRSDec24_individual_heat_pump_thermal_capacity', period)
        com_peak_load = buildings('F16_electric_PDRSDec24_com_peak_load', period)
        calculated_com_peak_load = 42 / com_peak_load

        confidence_factor = np.select(
            [
                individual_heat_pump_thermal_capacity >= 10,
                individual_heat_pump_thermal_capacity < 10
            ],
            [
                1,
                np.select(
                    [calculated_com_peak_load >= 1],
                    [1],
                    calculated_com_peak_load
                )
            ])

        return confidence_factor
    

class F16_electric_PDRSDec24_Ref_Elec(Variable):
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
        com_peak_load = buildings('F16_electric_PDRSDec24_com_peak_load', period)

        # we divide this by 1000 to convert MJ to GJ
        ref_elec = 365 * 0.905 * 1.05 * (com_peak_load / 1000)
        return ref_elec
    

class F16_electric_PDRSDec24_deemed_activity_gas_savings(Variable):
    #this is the deemed gas savings for a replacing electric equipment
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      HP_gas = buildings('F16_electric_PDRSDec24_HP_gas', period)
      capacity_factor = buildings('F16_electric_PDRSDec24_capacity_factor', period)
      confidence_factor = buildings('F16_electric_PDRSDec24_confidence_factor', period)
      lifetime = parameters(period).ESS.HEAB.table_F16_1.lifetime

      deemed_gas_savings = (-HP_gas) * capacity_factor * confidence_factor * (lifetime / 3.6)
      return deemed_gas_savings
    

class F16_electric_PDRSDec24_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        ref_elec = buildings('F16_electric_PDRSDec24_Ref_Elec', period)
        HP_elec = buildings('F16_electric_PDRSDec24_HP_elec', period)
        capacity_factor = buildings('F16_electric_PDRSDec24_capacity_factor', period)
        confidence_factor = buildings('F16_electric_PDRSDec24_confidence_factor', period)
        lifetime = parameters(period).ESS.HEAB.table_F16_1['lifetime']

        deemed_electricity_savings = (ref_elec - HP_elec) * capacity_factor * confidence_factor * (lifetime / 3.6)
        return deemed_electricity_savings


class F16_electric_PDRSDec24_energy_savings(Variable):
    value_type = float  
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #ref elec
        com_peak_load = buildings('F16_electric_PDRSDec24_com_peak_load', period)
        
        ref_elec = 365 * 0.905 * 1.05 * (com_peak_load / 1000)

        #HP elec
        HP_elec = buildings('F16_electric_PDRSDec24_HP_elec', period)

        #HP gas
        HP_gas = buildings('F16_electric_PDRSDec24_HP_gas', period)

        #capacity factor
        HP_Cap = buildings('F16_electric_PDRSDec24_HP_capacity_factor', period)
        WH_Cap = buildings('F16_electric_PDRSDec24_WH_capacity_factor', period)

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


class F16_electric_PDRSDec24_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        deemed_activity_electricity_savings = buildings('F16_electric_PDRSDec24_deemed_activity_electricity_savings', period)
        regional_network_factor = buildings('F16_electric_PDRSDec24_regional_network_factor', period)

        electricity_savings = deemed_activity_electricity_savings * regional_network_factor
        return electricity_savings


class F16_electric_PDRSDec24_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'output',
        'label' : 'The number of ESCs for WH1'
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('F16_electric_PDRSDec24_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        gas_savings = buildings('F16_electric_PDRSDec24_deemed_activity_gas_savings', period) #gas savings and deemed activity gas savings are the same value
        gas_certificate_conversion_factor = 0.47
        replacement_activity = buildings('F16_electric_PDRSDec24_replacement_activity', period)

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