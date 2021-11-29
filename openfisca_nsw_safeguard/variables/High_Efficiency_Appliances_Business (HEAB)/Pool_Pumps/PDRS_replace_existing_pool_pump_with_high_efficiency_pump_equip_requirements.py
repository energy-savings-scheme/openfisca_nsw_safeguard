from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021

class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_new_pump_has_minimum_warranty(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new pool pump have a warranty of three years or longer?'
    metadata = {
        'alias':  'New pump warranty length.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }

    def formula(buildings, period, parameters):
        warranty_length = buildings('ESS_HEAB_new_product_warranty_length', period)
        return (
            warranty_length >= 3
        )

class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_has_eligible_input_power(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new pool pump have an input power between 100W and 2500W?'
    metadata = {
        'alias':  'New pump has eligible input power.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }

    def formula(buildings, period, parameters):
        input_power = buildings('PDRS_new_pump_input_power', period)
        return (
                (
                    input_power >= 100
                ) *
                (
                    input_power <= 2500
                )
        )


class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_is_part_of_eligible_labelling_scheme(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the pool pump part of an eligible labelling scheme?'
    metadata = {
        'alias':  'New pump has eligible input power.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }



class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_new_pump_has_minimum_star_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new pool pump have a minimum star rating of 4.5 stars?'
    metadata = {
        'alias':  'New pump has minimum star rating.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }
    
    def formula(buildings, period, parameters):
        new_pump_star_rating = buildings('PDRS_new_pump_star_rating', period)
        return (
                new_pump_star_rating >= 4.5
                )


class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the Eligibility Requirements?'
    metadata = {
        'alias':  'PDRS Pool Pump Activity Meets Eligibility Requirements',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        has_minimum_warranty_length = buildings(
            'PDRS_replace_existing_pool_pump_with_high_efficiency_pump_new_pump_has_minimum_warranty', period)
        has_eligible_input_power = buildings(
            'PDRS_replace_existing_pool_pump_with_high_efficiency_pump_has_eligible_input_power', period)
        is_part_of_labelling_scheme = buildings(
            'PDRS_replace_existing_pool_pump_with_high_efficiency_pump_is_part_of_eligible_labelling_scheme', period)
        has_minimum_star_rating = buildings(
            'PDRS_replace_existing_pool_pump_with_high_efficiency_pump_new_pump_has_minimum_star_rating', period)
        return (
            has_minimum_warranty_length *
            has_eligible_input_power * 
            is_part_of_labelling_scheme * 
            has_minimum_star_rating
                )