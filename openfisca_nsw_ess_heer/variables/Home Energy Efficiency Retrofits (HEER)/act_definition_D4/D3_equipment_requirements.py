# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class D3_new_product_is_air_conditioner(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new product an air conditioner, as defined by AS/NZS 3823.2?'
    # what does it mean to be an air con in AS3823.2?


class D3_product_is_assigned_minimum_cooling_star_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the product been assigned a minimum cooling star rating,' \
            ' under AS/NZS 3823.2?'
    # note this is different from WERS Cooling/Heating Star Rating in D1/D2

    def formula(buildings, period, parameters):
        star_rating = buildings('air_con_cooling_rating', period)
        AirConCoolingRating = AS3823CoolingStarRating.possible_values  # imports functionality of AS3823CoolingStarRating enum from user_inputs
        no_rating = (star_rating == AS3823CoolingStarRating.no_rating)
        return (not(no_rating))


class D3_existing_unit_cooling_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the cooling capacity of the existing air conditioner, ' \
            ' in kW?'


class D3_new_unit_cooling_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the cooling capacity of the new air conditioner, ' \
            ' in kW?'


class new_unit_cooling_capacity_smaller_or_identical_to_old_unit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the replacement unit have a cooling capacity that is smaller' \
            ' or identical to the old unit?'

    def formula(buildings, period, parameters):
        existing_capacity = buildings('D3_existing_unit_cooling_capacity', period)
        new_capacity = buildings('D3_new_unit_cooling_capacity', period)
        return new_capacity <= existing_capacity


class D3_warranty_length(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the warranty length of the new air conditioner, in years?'


class D3_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the air conditioner has a minimum warranty length of' \
            ' 5 years, as required by Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        minimum_warranty_length = 5
        warranty_length = buildings('D3_warranty_length', period)
        return warranty_length >= minimum_warranty_length
