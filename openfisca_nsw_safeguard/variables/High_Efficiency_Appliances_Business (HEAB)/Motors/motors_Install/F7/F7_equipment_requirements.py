# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F7_end_user_equipment_is_3_phase_electric_motor(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment a three phase electric motor?'


class F7_end_user_equipment_is_high_efficiency(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment rated as a high efficiency product?'


class F7_end_user_equipment_is_high_efficiency_3_phase_motor(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment a 3 phase motor which is rated as' \
            ' high efficiency?'

    def formula(buildings, period, parameters):
        is_3_phase_motor = buildings('F7_end_user_equipment_is_3_phase_electric_motor', period)
        is_high_efficiency = buildings('F7_end_user_equipment_is_high_efficiency', period)
        return is_3_phase_motor * is_high_efficiency


class F7_is_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the electric motor registered in the GEMS Registry?'


class F7_complies_with_GEMS_2019(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the motor comply with the Greenhouse and Energy Minimum' \
            ' Standards (Three Phase Cage Induction Motors) Determination 2019?'


class F7_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F7?'

    def formula(buildings, period, parameters):
        is_high_efficiency_3_phase_motor = buildings('F7_end_user_equipment_is_high_efficiency_3_phase_motor', period)
        is_registered_in_GEMS = buildings('F7_is_registered_in_GEMS', period)
        complies_with_GEMS = buildings('F7_complies_with_GEMS_2019', period)
        return (is_high_efficiency_3_phase_motor * is_registered_in_GEMS * complies_with_GEMS)
