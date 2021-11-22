from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class PDRS_HEAB_install_or_replace_refrigerated_cabinet_peak_demand_savings(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What are the peak demand savings for the Refrigerated Cabinets activity?'
    metadata = {
        'alias':  'RC Peak Demand Savings',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        baseline_input_power = buildings('PDRS_HEAB_install_or_replace_refrigerated_cabinet_baseline_input_power', period)
        baseline_peak_adjustment_factor = (
                                    parameters(period).
                                    PDRS.table_A27_end_use_equipment_factors
                                    ['refrigerated_cabinets']['baseline_peak_load_adjustment_factor']
                                            )
        input_power = buildings('PDRS_HEAB_install_or_replace_refrigerated_cabinet_input_power', period)
        peak_load_adjustment_factor = (
                                    parameters(period).
                                    PDRS.table_A27_end_use_equipment_factors
                                    ['refrigerated_cabinets']['baseline_peak_load_adjustment_factor']
                                            )
        firmness_factor = (
                                    parameters(period).
                                    PDRS.table_A27_end_use_equipment_factors
                                    ['refrigerated_cabinets']['firmness_factor']
        )
        peak_demand_reduction_savings = (
                                (
                                    baseline_input_power *
                                    baseline_peak_adjustment_factor - 
                                    input_power *
                                    peak_load_adjustment_factor
                                ) *
                                firmness_factor
                            )
        meets_all_eligibility_criteria =  buildings('PDRS_HEAB_install_or_replace_refrigerated_cabinet_meets_all_eligibility_criteria', period)
        return(
                peak_demand_reduction_savings *
                meets_all_eligibility_criteria
                )


class PDRS_HEAB_install_or_replace_refrigerated_cabinet_baseline_input_power(Variable):
    value_type = bool
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
        baseline_EEI = (parameters(period).
        PDRS.refrigerated_cabinets.PDRS_refrigerated_cabinets_EEI_baselines[product_class])
        new_EEI = buildings(
            'new_refrigerated_cabinet_EEI')
        return (
            total_energy_consumption /
            24 * 
            (baseline_EEI / 
            new_EEI)
                )


class PDRS_HEAB_install_or_replace_refrigerated_cabinet_input_power(Variable):
    value_type = bool
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


class PDRS_HEAB_install_or_replace_refrigerated_cabinet_meets_all_eligibility_criteria(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Refrigerated Cabinets activity meet all of the eligibility criteria?'
    metadata = {
        'alias':  'RC Peak Demand Savings',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        meets_eligibility_requirements = buildings(
            'PDRS_HEAB_install_or_replace_refrigerated_cabinet_meets_eligibility_requirements', period)
        meets_equipment_requirements = buildings(
            'PDRS_HEAB_install_or_replace_refrigerated_cabinet_meets_equipment_requirements', period)
        meets_implementation_requirements = buildings(
            'PDRS_HEAB_install_or_replace_refrigerated_cabinet_meets_implementation_requirements', period)
        return (
                    meets_eligibility_requirements * 
                    meets_equipment_requirements *
                    meets_implementation_requirements
                )