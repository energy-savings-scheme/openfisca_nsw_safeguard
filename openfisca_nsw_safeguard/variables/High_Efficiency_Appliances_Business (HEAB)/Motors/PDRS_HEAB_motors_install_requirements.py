from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class PDRS_motor_install_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Equipment' \
            ' Requirements?'
    metadata = {
        'alias': "Install Motors meets equipment requirements",
        "regulation_reference": PDRS_2022["HEAB", "motors_install", "equipment"]
    }

    def formula(buildings, period, parameters):
        is_registered = buildings(
            'motor_registered_under_GEM', period)

        is_high_efficiency = buildings(
            'motor_3_phase_high_efficiency', period)


        return is_registered * is_high_efficiency 


class PDRS_motor_install_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Implementation' \
            ' Requirements?'
    metadata = {
        'alias': "Install Motors meets implementation requirements",
        "regulation_reference": PDRS_2022["HEAB", "motors_install", "implementation"]}

    def formula(buildings, period, parameters):
        is_installed = buildings(
            'Appliance_is_installed', period)
        rated_output = buildings('motors_rated_output', period)

        return (is_installed * 
                (rated_output >= 0.73) * (rated_output < 185)
                )

class PDRS_motor_install_meets_all_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the' \
            ' Requirements ?'
    metadata = {
        'alias': "PDRS Motors Install meets all requirements",
    }

    def formula(buildings, period, parameters):
        implementation = buildings(
            'PDRS_motor_install_meets_implementation_requirements', period)
        equipment = buildings(
            'PDRS_motor_install_meets_equipment_requirements', period)
        return implementation * equipment
