# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class B3_end_user_equipment_is_dishwasher(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a Dishwasher?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 1.'


class B3_end_user_equipment_is_labelled_for_energy_labelling(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment registered for energy labelling?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 2.'


class B3_end_user_equipment_has_registered_place_settings(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment have a number of place settings,' \
            ' recorded in the GEMS Registry?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        place_settings = buildings('B3_number_of_place_settings', period)
        condition_has_place_settings = (place_settings != 0 and place_settings is not None)
        return condition_has_place_settings


class B3_number_of_place_settings(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the number of place settings in the new End User Equipment?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B3, Equipment Requirement 3.'


class B3_meets_all_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet all of the Equipment' \
            ' Requirements detailed in Activity Definition B1?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1.'

    def formula(buildings, period, parameters):
        is_dishwasher = buildings('B3_end_user_equipment_is_dishwasher', period)
        is_labelled_for_energy_labelling = buildings('B3_end_user_equipment_is_labelled_for_energy_labelling', period)
        has_place_settings = buildings('B3_end_user_equipment_has_registered_place_settings', period)
        return (is_dishwasher * is_labelled_for_energy_labelling * has_place_settings)
