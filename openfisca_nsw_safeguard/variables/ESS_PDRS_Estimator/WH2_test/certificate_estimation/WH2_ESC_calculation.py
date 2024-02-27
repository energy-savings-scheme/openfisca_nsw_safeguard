from xml.etree import ElementInclude
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class WH2_test_capacity_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Capacity Factor'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      HP_cap = buildings('WH2_test_HP_capacity_factor', period)
      WH_cap = buildings('WH2_test_WH_capacity_factor', period)

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
    

class WH2_test_Ref_Elec(Variable):
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
        com_peak_load = buildings('WH2_test_com_peak_load', period)

        # we divide this by 1000 to convert MJ to GJ
        ref_elec = 365 * 0.905 * 1.05 * (com_peak_load / 1000)
        return ref_elec
    

class WH2_test_old_equipment_type(Enum):
    gas_water_boiler_heater = 'Gas-fired hot water boiler or heater'
    electric_water_boiler_heater = 'Electric resistance hot water boiler or heater'


class WH2_test_old_equipment(Variable):
    value_type = Enum
    entity = Building
    possible_values = WH2_test_old_equipment_type
    default_value = WH2_test_old_equipment_type.electric_water_boiler_heater
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label': 'Gas or electric water heater',
        'display_question' : 'Which type of equipment are you replacing?',
        'sorting' : 4
    }


class WH2_test_deemed_activity_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      refelec = buildings('WH2_test_Ref_Elec', period)
      HP_gas = buildings('WH2_test_HP_gas', period)
      capacity_factor = buildings('WH2_test_capacity_factor', period)
      lifetime = parameters(period).ESS.HEAB.table_F16_1.lifetime
      gas_or_electric_equipment = buildings('WH2_test_old_equipment', period)

      deemed_gas_savings = np.select(
        [
            gas_or_electric_equipment == WH2_test_old_equipment_type.gas_water_boiler_heater,
            gas_or_electric_equipment == WH2_test_old_equipment_type.electric_water_boiler_heater
        ],
        [
            ((refelec / 0.788)- HP_gas) * capacity_factor * (lifetime / 3.6),
            (-HP_gas) * capacity_factor * (lifetime / 3.6)
        ])
      
      return deemed_gas_savings
    

class WH2_test_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        ref_elec = buildings('WH2_test_Ref_Elec', period)
        HP_elec = buildings('WH2_test_HP_elec', period)
        capacity_factor = buildings('WH2_test_capacity_factor', period)
        lifetime = parameters(period).ESS.HEAB.table_F16_1['lifetime']
        gas_or_electric_equipment = buildings('WH2_test_old_equipment', period)

        deemed_electricity_savings = np.select(
        [
            gas_or_electric_equipment == WH2_test_old_equipment_type.gas_water_boiler_heater,
            gas_or_electric_equipment == WH2_test_old_equipment_type.electric_water_boiler_heater
        ],
        [
            (- HP_elec) * capacity_factor * (lifetime / 3.6),
            (ref_elec - HP_elec) * capacity_factor * (lifetime / 3.6)
        ])
        
        return deemed_electricity_savings

    
class WH2_test_energy_savings(Variable):
    value_type = float  
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #ref elec
        com_peak_load = buildings('WH2_test_com_peak_load', period)
        
        ref_elec = 365 * 0.905 * 1.05 * (com_peak_load / 1000)

        #HP elec
        HP_elec = buildings('WH2_test_HP_elec', period)

        #HP gas
        HP_gas = buildings('WH2_test_HP_gas', period)

        #capacity factor
        HP_Cap = buildings('WH2_test_HP_capacity_factor', period)
        WH_Cap = buildings('WH2_test_WH_capacity_factor', period)

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

        #gas or electric replacement equipment
        gas_or_electric_equipment = buildings('WH2_test_old_equipment',period)

        #gas savings
        deemed_gas_savings = np.select(
        [
            gas_or_electric_equipment == WH2_test_old_equipment_type.gas_water_boiler_heater,
            gas_or_electric_equipment == WH2_test_old_equipment_type.electric_water_boiler_heater
        ],
        [
            ((ref_elec / 0.788)- HP_gas) * capacity_factor * (lifetime / 3.6),
            (-HP_gas) * capacity_factor * (lifetime / 3.6)
        ])

        #electricity savings
        deemed_electricity_savings = np.select(
        [
            gas_or_electric_equipment == WH2_test_old_equipment_type.gas_water_boiler_heater,
            gas_or_electric_equipment == WH2_test_old_equipment_type.electric_water_boiler_heater
        ],
        [
            (- HP_elec) * capacity_factor * (lifetime / 3.6),
            (ref_elec - HP_elec) * capacity_factor * (lifetime / 3.6)
        ])

        annual_energy_savings = deemed_electricity_savings + deemed_gas_savings
        return annual_energy_savings


class WH2_test_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        deemed_activity_electricity_savings = buildings('WH2_test_deemed_activity_electricity_savings', period)
        regional_network_factor = buildings('WH2_test_regional_network_factor', period)

        electricity_savings = deemed_activity_electricity_savings * regional_network_factor
        return electricity_savings


class WH2_test_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'output',
        'label' : 'The number of ESCs for WH2_test'
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('WH2_test_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        gas_savings = buildings('WH2_test_deemed_activity_gas_savings', period) #gas savings and deemed activity gas savings are the same value
        gas_certificate_conversion_factor = 0.47
        replacement_activity = buildings('WH2_test_replacement_activity', period)

        WH2_test_eligible_ESCs = np.select(
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
                WH2_test_eligible_ESCs <= 0, WH2_test_eligible_ESCs > 0
            ],
            [
                0, WH2_test_eligible_ESCs
            ])
        return result_to_return