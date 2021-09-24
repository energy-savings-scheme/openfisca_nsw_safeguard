from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_HEER_showerheads_replace_new_end_user_equipment_is_showerhead(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'The End-User Equipment must be a showerhead as defined in' \
            ' AS/NZS 3662– Performance of showers for bathing.'  # IPART to define what this means


class ESS_HEER_showerheads_replace_WELS_rating(Variable):
    value_type = float  # need to check if this is Enum?
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the WELS rating of the showerhead.'


class ESS_HEER_showerheads_replace_showerhead_nominal_flow_rate(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the nominal flow rate of the showerhead, as tested' \
            ' according to AS/NZS 6400 – Water efficient products.'


class ESS_HEER_showerheads_replace_WELS_rating_and_flow_rating_are_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the showerhead has a minimum 3 star WELS rating' \
            ' and a nominal flow rate of less than or equal to 6 litres a' \
            ' minute, as required by Equipment Requirement 2.'

    def formula(buildings, period, parameters):
        WELS_rating = buildings('ESS_HEER_showerheads_replace_WELS_rating', period)
        nominal_flow_rating = buildings('ESS_HEER_showerheads_replace_showerhead_nominal_flow_rate', period)
        condition_minimum_WELS_rating = WELS_rating > 3 # need to rewrite as parameter
        condition_nominal_flow_rating = nominal_flow_rating <= 6 # need to rewrite as parameter
        return condition_minimum_WELS_rating * condition_nominal_flow_rating


class ESS_HEER_showerheads_replace_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the showerhead has a minimum warranty length of' \
            ' 2 years, as required by Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('ESS_HEER_new_product_warranty_length', period)
        return warranty_length >= 2 # need to rewrite as parameter


class ESS_HEER_showerheads_replace_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Implementation meet the Equipment Requirements detailed' \
            ' in Activity Definition E6?'

    def formula(buildings, period, parameters):
        new_equipment_is_showerhead = buildings(
        'ESS_HEER_showerheads_replace_new_end_user_equipment_is_showerhead', period)
        has_minimum_WELS_and_flow_rating = buildings(
        'ESS_HEER_showerheads_replace_WELS_rating_and_flow_rating_are_eligible', period)
        has_minimum_warranty = buildings(
        'ESS_HEER_showerheads_replace_minimum_warranty_length', period)
        return (
        new_equipment_is_showerhead *
        has_minimum_WELS_and_flow_rating *
        has_minimum_warranty
        )
