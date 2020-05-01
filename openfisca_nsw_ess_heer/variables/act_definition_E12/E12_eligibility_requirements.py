# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E12_site_must_be_residential(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'The External Blind must be installed to a door or window' \
            ' in a Residential or Small Building Site, as prescribed in ' \
            ' Eligiblity Requirement 1. '  # IPART to define what this means and how to measure this. need to build building type enum and refer into this

    def formula(buildings, period, parameters):
        building_type = buildings('building_type', period)
        BuildingType = building_type.possible_values  # imports functionality of climate zone enum from user_inputs
        is_residential = (building_type == BuildingType.residential_building)
        return is_residential


class existing_exhaust_fan_is_present(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether an existing exhaust fan is present at the site,' \
            ' as required in Eligiblity Requirement 2 in Activity' \
            ' Definition E12.'


class exhaust_fan_exhausts_to_outside(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the exhaust fan exhausts directly to the outside of' \
            ' the building, as required in Eligiblity Requirement 3 in Activity' \
            ' Definition E12.'
