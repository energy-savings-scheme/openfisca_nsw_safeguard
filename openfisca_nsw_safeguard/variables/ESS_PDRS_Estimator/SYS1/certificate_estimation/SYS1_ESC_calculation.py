from xml.etree import ElementInclude
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class SYS1_asset_life(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = "High Efficiency Motor Asset Life"
    metadata = {
        'variable-type': 'inter-interesting',
        'label': "High Efficiency Motor Asset Life"
    }
    
    def formula(buildings, period, parameters):
        rated_output = buildings('SYS1_new_equipment_rated_output', period)
        rated_output_band = np.select([
            (rated_output < 0.73), 
            ((rated_output >= 0.73) * (rated_output < 2.6)),    
            ((rated_output >= 2.6) * (rated_output < 9.2)),    
            ((rated_output >= 9.2) * (rated_output < 41)),    
            ((rated_output >= 41) * (rated_output < 100)),    
            ((rated_output >= 100) * (rated_output < 185)),    
            (rated_output > 185), 
        ],
        [
            'under_0.73_kW',
            '0.73_to_2.6kW',
            '2.6_to_9.2kW',
            '9.2_to_41kW',
            '41_to_100kW',
            '100_to_185kW',
            'over_185kW'
        ]
        )
        asset_life = parameters(period).ESS.HEAB.table_F7_4['asset_life'][rated_output_band]        
        return asset_life


class SYS1_load_utilisation_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input power (kW)'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        rated_output = buildings('SYS1_new_equipment_rated_output', period)        
        SYS1_business_classification = buildings('SYS1_business_classification', period)
        SYS1_end_user_service = buildings('SYS1_end_user_service', period)
        
        rated_output = np.select([
            (rated_output < 0.73), 
            ((rated_output >= 0.73) * (rated_output < 2.6)),    
            ((rated_output >= 2.6) * (rated_output < 9.2)),    
            ((rated_output >= 9.2) * (rated_output < 41)),    
            ((rated_output >= 41) * (rated_output < 100)),    
            ((rated_output >= 100) * (rated_output < 185)),    
            (rated_output > 185), 
        ],
        [
            'under_0.73_kW',
            '0.73_to_2.6kW',
            '2.6_to_9.2kW',
            '9.2_to_41kW',
            '41_to_100kW',
            '100_to_185kW',
            'over_185kW'
        ]
        )
        print("SYS1_business_classification", SYS1_business_classification)
        print("SYS1_end_user_service",  SYS1_end_user_service)
        load_utilisation_factor = (parameters(period).ESS.HEAB.table_F7_1['load_utilisation_factor'][SYS1_business_classification][SYS1_end_user_service])

        load_utilisation_factor = np.where(load_utilisation_factor == 0,
        (parameters(period).ESS.HEAB.table_F7_2['load_utilisation_factor'][rated_output]), load_utilisation_factor)

        return load_utilisation_factor


class SYS1_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        SYS1_new_equipment_rated_output = buildings('SYS1_new_equipment_rated_output', period)
        SYS1_baseline_efficiency = buildings('SYS1_baseline_efficiency', period)
        SYS1_new_efficiency = buildings('SYS1_new_efficiency', period)
        SYS1_load_utilisation_factor = buildings('SYS1_load_utilisation_factor', period)
        SYS1_asset_life = buildings('SYS1_asset_life', period)

        temp_calc_1 = ( SYS1_new_equipment_rated_output / (SYS1_baseline_efficiency / 100))
        print(temp_calc_1)
        temp_calc_2 = ( SYS1_new_equipment_rated_output / (SYS1_new_efficiency / 100))
        print(temp_calc_2)
        temp_calc_3 = (SYS1_load_utilisation_factor * SYS1_asset_life * ( 8760 / 1000 ))
        print(temp_calc_3)
        return ((temp_calc_1 - temp_calc_2) * temp_calc_3)


class SYS1_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('SYS1_deemed_activity_electricity_savings', period)
        print(deemed_electricity_savings)
        regional_nw_factor = buildings('SYS1_regional_network_factor', period)
        return deemed_electricity_savings * regional_nw_factor


class SYS1_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for WH1'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('SYS1_electricity_savings', period)
        print(electricity_savings)
        electricity_certificate_conversion_factor = 1.06

        result = (electricity_savings * electricity_certificate_conversion_factor)
        result_to_return = np.select([
                result < 0, result > 0
            ], [
                0, result
            ])
        return result_to_return
