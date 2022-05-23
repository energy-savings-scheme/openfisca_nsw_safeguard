from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021

import numpy as np

class PDRS_replace_existing_pool_pump_new_product_is_for_domestic_use(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product for domestic use in a pool or spa?'
    metadata = {
        'alias':  'New product for domestic use.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }


class PoolPumpType(Enum):
    single_speed_pool_pump = 'Heat pump is a single speed heat pump.'
    dual_speed_heat_pump = 'Heat pump is a dual speed heat pump.'
    multiple_speed_pool_pump = 'Heat pump is a multiple speed heat pump.'
    variable_speed_pool_pump = 'Heat pump is a variable speed heat pump.'
    not_eligible_pool_pump = 'Product is not a heat pump, or is not any of the above types of heat pump.'


class ESS_and_PDRS_new_pool_pump_type(Variable):
    value_type = Enum
    default_value = PoolPumpType.single_speed_pool_pump
    possible_values = PoolPumpType
    entity = Building
    definition_period = ETERNITY
    label = 'What is the type of heat pump that is being replaced?'
    metadata = {
        'alias':  'New pool pump type.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }


class PDRS_replace_existing_pool_pump_new_pump_is_eligible_type(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new pool pump an eligible type to be used in this activity?'

    def formula(buildings, period, parameters):
        new_pool_pump_type = buildings('ESS_and_PDRS_new_pool_pump_type', period)
        PoolPumpType = new_pool_pump_type.possible_values
        not_eligible_pool_pump_type = (new_pool_pump_type == PoolPumpType.not_eligible_pool_pump)
        return np.logical_not(not_eligible_pool_pump_type)


class PDRS_replace_existing_pool_pump_pool_pump_has_eligible_input_power(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the existing pool pump has a power between 100W and 2500W?'

    def formula(buildings, period, parameters):
        input_power_in_W = (
            buildings('PDRS_replace_existing_pool_pump_with_high_efficiency_pump_input_power', period) *
            1000
        ) # input power in Table SYS2.2 is calculated in kW
        return (
            (input_power_in_W > 100) *
            (input_power_in_W < 2500)
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
        new_pump_star_rating = buildings('ESS_and_PDRS_new_pump_star_rating', period)
        pump_star_rating = new_pump_star_rating.possible_values

        has_minimum_star_rating = (
                (new_pump_star_rating == pump_star_rating.four_and_a_half_stars) +
                (new_pump_star_rating == pump_star_rating.five_stars) +
                (new_pump_star_rating == pump_star_rating.five_and_a_half_stars) +
                (new_pump_star_rating == pump_star_rating.six_stars) +
                (new_pump_star_rating == pump_star_rating.six_and_a_half_stars) +
                (new_pump_star_rating == pump_star_rating.seven_stars) +
                (new_pump_star_rating == pump_star_rating.seven_and_a_half_stars) +
                (new_pump_star_rating == pump_star_rating.eight_stars) +
                (new_pump_star_rating == pump_star_rating.eight_and_a_half_stars) +
                (new_pump_star_rating == pump_star_rating.nine_stars) +
                (new_pump_star_rating == pump_star_rating.nine_and_a_half_stars) +
                (new_pump_star_rating == pump_star_rating.ten_stars)
                )
        return has_minimum_star_rating


class PDRS_new_pump_warranty_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the warranty length for the new pool pump, in years?'
    metadata = {
        'alias':  'PDRS Pool Pump Warranty Length',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }


class PDRS_replace_existing_pool_pump_new_pump_has_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new pool pump has a warranty length of at least 3 years?'
    metadata = {
        'alias':  'PDRS Pool Pump Has Minimum Warranty Length',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }

    def formula(buildings, period, parameters):
        new_warranty_length = buildings('PDRS_new_pump_warranty_length', period)
        return (new_warranty_length >= 3)


class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the Eligibility Requirements?'
    metadata = {
        'alias':  'PDRS Pool Pump Activity Meets Eligibility Requirements',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        for_domestic_use = buildings(
            'PDRS_replace_existing_pool_pump_new_product_is_for_domestic_use', period)
        eligible_type_of_pool_pump = buildings(
            'PDRS_replace_existing_pool_pump_new_pump_is_eligible_type', period)
        has_minimum_warranty_length = buildings(
            'PDRS_replace_existing_pool_pump_new_pump_has_minimum_warranty_length', period)
        has_eligible_input_power = buildings(
            'PDRS_replace_existing_pool_pump_pool_pump_has_eligible_input_power', period)
        is_part_of_labelling_scheme = buildings(
            'PDRS_replace_existing_pool_pump_with_high_efficiency_pump_is_part_of_eligible_labelling_scheme', period)
        has_minimum_star_rating = buildings(
            'PDRS_replace_existing_pool_pump_with_high_efficiency_pump_new_pump_has_minimum_star_rating', period)
        return (
            for_domestic_use *
            eligible_type_of_pool_pump *
            has_minimum_warranty_length *
            has_eligible_input_power *
            is_part_of_labelling_scheme *
            has_minimum_star_rating
                )