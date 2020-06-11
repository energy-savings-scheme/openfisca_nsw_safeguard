# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class B2_end_user_equipment_is_clothes_dryer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a Clothes Dryer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B2, Equipment Requirement 1.'


class B2_end_user_equipment_is_labelled_for_energy_labelling(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment registered for energy labelling?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B2, Equipment Requirement 2.'


class B2_end_user_equipment_is_not_combination_washer_dryer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment not a combination washer/dryer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 3.'
    #  long term - need to build a "product type" enum and make this "!= combination washer dryer"

    def formula(buildings, period, parameters):
        is_washer_dryer = buildings('B2_end_user_equipment_is_combination_washer_dryer', period)
        return (not(is_washer_dryer))


class B2_end_user_equipment_has_a_load(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment has a load, as recorded in the' \
            ' GEMS Registry?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 4.'

    def formula(buildings, period, parameters):
        equipment_load = buildings('B2_end_user_equipment_load', period)
        condition_has_load = (equipment_load != 0 and equipment_load is not None)
        return condition_has_load


class B2_end_user_equipment_load(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the equipment load of the new end user equipment, in kilograms?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 4.'


class B2_end_user_equipment_is_combination_washer_dryer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a combination washer/dryer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 5.'


class B2_meets_all_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet all of the Equipment' \
            ' Requirements detailed in Activity Definition B1?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1.'

    def formula(buildings, period, parameters):
        is_clothes_dryer = buildings('B2_end_user_equipment_is_clothes_dryer', period)
        is_labelled_for_energy_labelling = buildings('B2_end_user_equipment_is_labelled_for_energy_labelling', period)
        is_not_washer_dryer = buildings('B2_end_user_equipment_is_not_combination_washer_dryer', period)
        has_load = buildings('B2_end_user_equipment_has_a_load', period)
        return (is_clothes_dryer * is_labelled_for_energy_labelling
        * is_not_washer_dryer * has_load)
