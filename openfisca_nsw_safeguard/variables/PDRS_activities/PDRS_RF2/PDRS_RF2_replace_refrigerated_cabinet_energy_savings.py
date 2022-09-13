from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class PDRS_RF2_replace_refrigerated_cabinet_peak_demand_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the peak demand savings for the Refrigerated Cabinets activity?'
    metadata = {
        'alias':  'RC Peak Demand Savings',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        baseline_input_power = buildings('PDRS_RF2_replace_refrigerated_cabinet_baseline_input_power', period)
        baseline_peak_adjustment_factor = (buildings
        ('PDRS_RF2_replace_refrigerated_cabinet_baseline_peak_adjustment_factor', period))
        input_power = buildings('PDRS_RF2_replace_refrigerated_cabinet_input_power', period)
        peak_load_adjustment_factor = baseline_peak_adjustment_factor
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor.firmness_factor['RF2']
        peak_demand_reduction_savings = (
                                (
                                    baseline_input_power *
                                    baseline_peak_adjustment_factor - 
                                    input_power *
                                    peak_load_adjustment_factor
                                ) *
                                firmness_factor
                            )
        meets_all_eligibility_criteria =  buildings('PDRS_RF2_replace_refrigerated_cabinet_meets_all_eligibility_criteria', period)
        return(
                peak_demand_reduction_savings *
                meets_all_eligibility_criteria
                )


class PDRS_RF2_replace_refrigerated_cabinet_baseline_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the baseline input power for the Refrigerated Cabinets activity?'
    metadata = {
        'alias':  'RC Baseline Input Power',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        total_energy_consumption = buildings(
            'new_refrigerated_cabinet_total_energy_consumption', period)
        product_class = buildings('refrigerated_cabinet_product_class', period)
        duty_class = buildings('refrigerated_cabinet_duty_class', period)
        adjustment_factor = parameters(period).PDRS.refrigerated_cabinets.table_RF2_1['adjustment_factor'][product_class][duty_class]
        baseline_EEI = parameters(period).PDRS.refrigerated_cabinets.table_RF2_1['baseline_EEI'][product_class][duty_class]
        new_EEI = buildings(
            'new_refrigerated_cabinet_EEI', period)
        return (
                total_energy_consumption *
                adjustment_factor *
                (
                    baseline_EEI /
                    new_EEI
                ) /
                24
                )


class PDRS_RF2_replace_refrigerated_cabinet_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the input power for the Refrigerated Cabinets activity?'
    metadata = {
        'alias':  'RC Input Power',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        total_energy_consumption = buildings(
            'new_refrigerated_cabinet_total_energy_consumption', period)
        return (
            total_energy_consumption /
            24 
                )


class PDRS_RF2_replace_refrigerated_cabinet_baseline_peak_adjustment_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the baseline peak adjustment factor for the Refrigerated Cabinets activity?'
    metadata = {
        'alias':  'RC Input Power',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        product_type = buildings('refrigerated_cabinet_product_type', period)
        duty_class = buildings('refrigerated_cabinet_duty_class', period)
        temperature_factor = (parameters(period).
        PDRS.refrigerated_cabinets.table_RF2_2.temperature_factor[product_type][duty_class])
        usage_factor = 1
        return (
            (temperature_factor) * 
            (usage_factor)
        )



class PDRS_RF2_replace_refrigerated_cabinet_meets_all_eligibility_criteria(Variable):
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
            'PDRS_RF2_replace_refrigerated_cabinet_meets_eligibility_requirements', period)
        meets_equipment_requirements = buildings(
            'PDRS_RF2_replace_refrigerated_cabinet_meets_equipment_requirements', period)
        meets_implementation_requirements = buildings(
            'PDRS_RF2_replace_refrigerated_cabinet_meets_implementation_requirements', period)
        return (
                    meets_eligibility_requirements * 
                    meets_equipment_requirements *
                    meets_implementation_requirements
                )