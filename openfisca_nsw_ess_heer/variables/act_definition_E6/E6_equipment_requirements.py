# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E6_new_end_user_equipment_is_showerhead(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'The End-User Equipment must be a showerhead as defined in' \
            ' AS/NZS 3662– Performance of showers for bathing.'  #IPART to define what this means


class WELS_rating(Variable):
    value_type = float  # need to check if this is Enum?
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the WELS rating of the showerhead.'


class showerhead_nominal_flow_rate(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the nominal flow rate of the showerhead, as tested' \
            ' according to AS/NZS 6400 – Water efficient products.'


class WELS_rating_and_flow_rating_are_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the showerhead has a minimum 3 star WELS rating' \
            ' and a nominal flow rate of less than or equal to 6 litres a' \
            ' minute, as required by Equipment Requirement 2.'

    def formula(buildings, period, parameters):
        WELS_rating = buildings('WELS_rating', period)
        nominal_flow_rating = buildings('showerhead_nominal_flow_rate', buildings)
        condition_minimum_WELS_rating = WELS_rating > 3
        condition_nominal_flow_rating = nominal_flow_rating <= 6
        return condition_minimum_WELS_rating * condition_nominal_flow_rating


class warranty_length(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the warranty length of the showerhead, in years.'


class minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the showerhead has a minimum warranty length of' \
            ' 2 years, as required by Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('warranty_length', period)
        return warranty_length >= 2
