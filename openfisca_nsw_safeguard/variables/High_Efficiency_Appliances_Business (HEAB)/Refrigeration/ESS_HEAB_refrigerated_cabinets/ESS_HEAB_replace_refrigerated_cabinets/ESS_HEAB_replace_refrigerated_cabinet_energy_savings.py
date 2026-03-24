import numpy as np

from openfisca_core.periods import ETERNITY

from openfisca_nsw_safeguard.entities import Building
from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class ESS_HEAB_replace_refrigerated_cabinet_electricity_savings(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the peak demand savings for the Refrigerated Cabinets activity?'
    metadata = {
        'alias':  'RC Peak Demand Savings',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        total_energy_consumption = buildings(
            'new_refrigerated_cabinet_total_energy_consumption', period)
        product_class = buildings(
            'refrigerated_cabinet_product_class', period)
        duty_class = buildings(
            'refrigerated_cabinet_duty_class', period) 
        baseline_EEI = parameters(period).ESS.HEAB.table_F1_2_1.baseline_EEI[product_class][duty_class]
        product_EEI = buildings(
            'new_refrigerated_cabinet_EEI', period)
        total_display_area = buildings('new_refrigerated_cabinet_total_display_area', period)

        total_display_area = np.where(total_display_area < 3.3, 
                                        'less_than_3_3m2', 
                                        '3_3m2_or_greater'
                                        )

        adjustment_factor = parameters(period).ESS.HEAB.table_F1_2_1.adjustment_factor[product_class][duty_class]
        product_lifetime = parameters(period).ESS.HEAB.table_F1_2_2.lifetime[product_class][total_display_area]
        energy_savings =    (
                                total_energy_consumption *
                                (
                                    baseline_EEI /
                                    product_EEI -
                                    1
                                ) * 
                                adjustment_factor *
                                365 *
                                product_lifetime /
                                1000
                            )
        meets_all_eligibility_criteria =  buildings('ESS_HEAB_replace_refrigerated_cabinet_meets_all_eligibility_criteria', period)
        return(
                energy_savings *
                meets_all_eligibility_criteria
                )


class ESS_HEAB_replace_refrigerated_cabinet_meets_all_eligibility_criteria(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Refrigerated Cabinets activity meet all of the eligibility criteria?'
    metadata = {
        'alias':  'RC Peak Demand Savings',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        meets_eligibility_requirements = buildings(
            'ESS_HEAB_replace_refrigerated_cabinet_meets_eligibility_requirements', period)
        meets_equipment_requirements = buildings(
            'ESS_HEAB_replace_refrigerated_cabinet_meets_equipment_requirements', period)
        return (
                    meets_eligibility_requirements * 
                    meets_equipment_requirements
                )