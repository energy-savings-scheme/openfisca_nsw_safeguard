from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022
import numpy as np


class ESS_HEAB_install_high_efficiency_motor_electricity_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "HEAB Motors Install The Peak demand savings "
    metadata = {
        "alias": "HEAB Motors Install Peak demand savings",
        "regulation_reference": PDRS_2022["HEAB", "motors_install", "energy_savings"]
    }

    def formula(building, period, parameters):

        meets_all_requirements = building(
            'ESS__HEAB_install_new_high_efficiency_motor_meets_all_requirements', period)
        savings = building("ESS_HEAB_install_high_efficiency_motor_equipment_deemed_electricity_savings", period)

        return meets_all_requirements * savings


class ESS_HEAB_install_high_efficiency_motor_equipment_deemed_electricity_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "Electricity savings created by installing a new High Efficiency Motor within Activity Definition F7."
    metadata = {
        "alias": "Motors Peak demand savings",
        "regulation_reference": PDRS_2022["XX", "motors"]
    }

    def formula(buildings, period, parameters):
        rated_output = buildings('motors_rated_output', period)
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
        baseline_efficiency = buildings('PDRS__motors__existing_motor_efficiency', period)
        new_efficiency = buildings('PDRS__motors__new_efficiency', period)
        load_utilisation_factor = buildings('ESS_HEAB_install_high_efficiency_motor_load_utilisation_factor', period)
        asset_life = parameters(period).ESS.HEAB.table_F7_4.asset_life[rated_output_band]
        hours_in_year = parameters(period).ESS.ESS_related_constants.hours_in_year

        electricity_savings = (
                                (
                                    rated_output /
                                    (
                                        baseline_efficiency / 100
                                    )
                                ) -
                                (
                                    rated_output /
                                    (
                                        new_efficiency / 100
                                    )
                                ) *
                                load_utilisation_factor *
                                asset_life *
                                hours_in_year /
                                1000
                                )
        
        return electricity_savings


class ESS_HEAB_install_high_efficiency_motor_load_utilisation_factor(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = 'What is the Load Utilisation Factor relevant to installing' \
            ' a new High Efficiency Motor within Activity Definition F7,' \
            ' as identified in Table F7.1 or F7.2?'
    metadata = {
        "alias": "Motors Peak demand savings",
        "regulation_reference": PDRS_2022["XX", "motors"]
    }

    def formula(buildings, period, parameters):
        business_classification = buildings('ANZSIC_business_classification', period)
        end_use_service = buildings('ESS_PDRS_End_Use_Service', period)
        rated_output = buildings('motors_rated_output', period)
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

        load_utilisation_factor = (parameters(period).ESS.HEAB.table_F7_1.load_utilisation_factor
        [business_classification][end_use_service])
        load_utilisation_factor = np.where(load_utilisation_factor == 0,
        (parameters(period).ESS.HEAB.table_F7_2.load_utilisation_factor[rated_output]),
        load_utilisation_factor)

        return load_utilisation_factor