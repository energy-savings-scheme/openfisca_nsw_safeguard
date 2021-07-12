from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS__SONA_end_user_equipment_is_clothes_dryer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a Clothes Dryer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B2, Equipment Requirement 1.'


    def formula(buildings, period, parameters):
        equipment_type = buildings('ESS__SONA_equipment_type', period)
        possible_equipment_type = equipment_type.possible_values
        is_dryer = (equipment_type == possible_equipment_type.dryer)
        return is_dryer


class ESS__SONA_end_user_equipment_is_combination_washer_dryer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a combination washer/dryer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 3.'
    #  long term - need to build a "product type" enum and make this "!= combination washer dryer"


class ESS__SONA_dryer_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet all of the Equipment' \
            ' Requirements detailed in Activity Definition B1?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1.'

    def formula(buildings, period, parameters):
        is_clothes_dryer = buildings('ESS__SONA_end_user_equipment_is_clothes_dryer', period)
        is_not_washer_dryer = np.logical_not(buildings('ESS__SONA_end_user_equipment_is_combination_washer_dryer', period))
        is_labelled_for_energy_labelling = buildings('ESS__SONA_equipment_labelled_for_energy_labelling', period)
        return (is_clothes_dryer *
                is_not_washer_dryer *
                is_labelled_for_energy_labelling)
