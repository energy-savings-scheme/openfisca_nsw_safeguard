from xml.etree import ElementInclude
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class F17_individual_heat_pump_thermal_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Individual Heat Pump Thermal Capacity (kW)'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        total_heat_pump_thermal_capacity = buildings('F17_total_heat_pump_thermal_capacity', period)
        number_of_heat_pumps = buildings('F17_number_of_heat_pumps', period)
        individual_heat_pump_thermal_capacity = total_heat_pump_thermal_capacity / number_of_heat_pumps

        return individual_heat_pump_thermal_capacity
    

class F17_confidence_factor(Variable):
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
        individual_heat_pump_thermal_capacity = buildings('F17_individual_heat_pump_thermal_capacity', period)
        com_peak_load = buildings('F17_com_peak_load', period)
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


class F17_Ref_Elec(Variable):
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
        com_peak_load = buildings('F17_com_peak_load', period)

        # we divide this by 1000 to convert MJ to GJ
        ref_elec = 365 * 0.905 * 1.05 * (com_peak_load / 1000)
        return ref_elec


class F17_deemed_activity_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      ref_elec = buildings('F17_Ref_Elec', period)  
      HP_gas = buildings('F17_HP_gas', period)
      confidence_factor = buildings('F17_confidence_factor', period)
      lifetime = parameters(period).ESS.HEAB.table_F16_1.lifetime

      deemed_gas_savings = (ref_elec / 0.85 -HP_gas) * confidence_factor * lifetime / 3.6
      return deemed_gas_savings


class F17_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        HP_elec = buildings('F17_HP_elec', period)
        confidence_factor = buildings('F17_confidence_factor', period)
        lifetime = parameters(period).ESS.HEAB.table_F16_1['lifetime']

        deemed_electricity_savings = (- HP_elec) * confidence_factor * lifetime / 3.6
        return deemed_electricity_savings


class F17_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        deemed_activity_electricity_savings = buildings('F17_deemed_activity_electricity_savings', period)
        regional_network_factor = buildings('F17_regional_network_factor', period)

        electricity_savings = deemed_activity_electricity_savings * regional_network_factor
        return electricity_savings


class F17_annual_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }
        
    def formula(buildings, period, parameters):
        HP_elec = buildings('F17_HP_elec', period)
        lifetime = parameters(period).ESS.HEAB.table_F16_1['lifetime']
        com_peak_load = buildings('F17_com_peak_load', period)
        HP_gas = buildings('F17_HP_gas', period)
        confidence_factor = buildings('F17_confidence_factor', period)

        #deemed electricity savings
        deemed_electricity_savings = (- HP_elec) * confidence_factor * lifetime / 3.6

        #ref elec
        ref_elec = 365 * 0.905 * 1.05 * (com_peak_load / 1000)

        #deemed gas savings
        deemed_gas_savings = (ref_elec / 0.85 - HP_gas) * confidence_factor * lifetime / 3.6

        #annual energy savings
        annual_energy_savings = deemed_electricity_savings + deemed_gas_savings

        annual_savings_return = np.select([
                annual_energy_savings <= 0, 
                annual_energy_savings > 0
            ],
            [
                0, 
                annual_energy_savings
            ])
        
        return annual_savings_return


class F17_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'output',
        'label' : 'The number of ESCs for F17'
    }

    def formula(buildings, period, parameters):
        installation_eligibility = buildings('F17_installation_activity', period)
        electricity_savings = buildings('F17_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        gas_savings = buildings('F17_deemed_activity_gas_savings', period) #gas savings and deemed activity gas savings are the same value
        gas_certificate_conversion_factor = 0.47
        
        F17_eligible_ESCs = np.select(
            [
                installation_eligibility,
                np.logical_not(installation_eligibility)
            ],
            [
                (electricity_savings * electricity_certificate_conversion_factor) + (gas_savings * gas_certificate_conversion_factor),
                0
            ])


        result_to_return = np.select(
            [
                F17_eligible_ESCs <= 0,
                F17_eligible_ESCs > 0
            ],
            [
                0,
                F17_eligible_ESCs
            ])
        return result_to_return