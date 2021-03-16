# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

#  need to build logic through Enum to ask whether a door or window is being replaced


class existing_window_is_single_glazed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing window single glazed?'


class existing_door_is_fully_single_glazed_framed_unit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing door a fully single glazed framed unit?'


class existing_door_is_fully_single_glazed_framed_unit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing door a fully single glazed framed unit?'


class existing_window_is_external(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing window external?'


class existing_door_is_external(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing door external?'


class is_residential_or_small_business_site(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the site a Residential or Small Business Site?'

    def formula(buildings, period, parameters):
        building_type = buildings('building_type', period)
        BuildingType = building_type.possible_values
        is_residential = (building_type == BuildingType.residential_building)
        is_small_business = (building_type == BuildingType.small_business_site)
        return is_residential + is_small_business



class D1_all_eligibility_requirements_are_true(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the eligibility requirements?'

    def formula(buildings, period, parameters):
        existing_window_is_single_glazed = buildings('existing_window_is_single_glazed', period)
        existing_door_is_fully_single_glazed_framed_unit = buildings('existing_door_is_fully_single_glazed_framed_unit', buildings)
        existing_window_is_external = buildings('existing_window_is_external', period)
        existing_door_is_external = buildings('existing_door_is_external', period)
        is_residential_or_small_business = buildings('is_residential_or_small_business_site', period)
        return (((existing_window_is_single_glazed * existing_window_is_external)
        + (existing_door_is_fully_single_glazed_framed_unit * existing_door_is_external))
        * is_residential_or_small_business)

        # note that this does not reflect what is actually written, but rather \
        # what the perceived intent of this activity - that you're replacing \
        # either a window OR a door - is intended to achieve
