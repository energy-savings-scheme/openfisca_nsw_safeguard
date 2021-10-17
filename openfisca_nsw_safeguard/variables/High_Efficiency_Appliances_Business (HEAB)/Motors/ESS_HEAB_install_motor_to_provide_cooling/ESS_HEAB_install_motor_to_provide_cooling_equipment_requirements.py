from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Building


class ESS_HEAB_install_motor_to_provide_cooling_is_electronically_communtated_motor(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product an electronically communtated (brushless DC) motor?'


class ESS_HEAB_install_motor_to_provide_cooling_nominal_input_power_less_than_500W(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the nominal input power of the new End User Equipment less than' \
            ' or equal to 500W?'

    def formula(buildings, period, parameters):
        equipment_input_power = buildings('new_motor_nominal_input_power', period)
        condition_less_than_500W = (equipment_input_power <= 500)
        return condition_less_than_500W


class ESS_HEAB_install_motor_to_provide_cooling_output_power_greater_than_existing_fan(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the output power of the new equipment equal or greater than the' \
            ' existing equipment?'

    def formula(buildings, period, parameters):
        existing_output_power = buildings('existing_motor_equipment_output_power', period)
        new_output_power = buildings('new_motor_equipment_output_power', period)
        condition_new_power_higher_than_existing = (new_output_power >= existing_output_power)
        return condition_new_power_higher_than_existing


class ESS_HEAB_install_motor_to_provide_cooling_airflow_volume_greater_than_existing_fan(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the airflow volume of the new equipment equal or greater than the' \
            ' existing equipment?'

    def formula(buildings, period, parameters):
        existing_airflow_volume = buildings('existing_motor_equipment_airflow_volume', period)
        new_airflow_volume = buildings('new_motor_equipment_airflow_volume', period)
        condition_new_airflow_volume_higher_than_existing = (new_airflow_volume >= existing_airflow_volume)
        return condition_new_airflow_volume_higher_than_existing


class ESS_HEAB_install_motor_to_provide_cooling_output_power_or_airflow_greater_than_existing_fan(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the output power or the airflow volume of the new equipment' \
            ' equal or greater than the existing equipment?'

    def formula(buildings, period, parameters):
        output_power_greater = buildings('ESS_HEAB_install_motor_to_provide_cooling_output_power_greater_than_existing_fan', period)
        airflow_greater = buildings('ESS_HEAB_install_motor_to_provide_cooling_airflow_volume_greater_than_existing_fan', period)
        return output_power_greater + airflow_greater


class ESS_HEAB_install_motor_to_provide_cooling_meets_other_scheme_administrator_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product meet any other requirements specified by the' \
            ' Scheme Administrator, including the suitability of the impeller' \
            ' for the motor?'
    # what does complying with this Determination mean?


class ESS_HEAB_install_motor_to_provide_cooling_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F5?'

    def formula(buildings, period, parameters):
        is_electronically_communtated_motor = buildings('ESS_HEAB_install_motor_to_provide_cooling_is_electronically_communtated_motor', period)
        input_less_than_500W = buildings('ESS_HEAB_install_motor_to_provide_cooling_nominal_input_power_less_than_500W', period)
        higher_output_or_airflow = buildings('ESS_HEAB_install_motor_to_provide_cooling_output_power_or_airflow_greater_than_existing_fan', period)
        meets_other_requirements = buildings('ESS_HEAB_install_motor_to_provide_cooling_meets_other_scheme_administrator_requirements', period)
        return (is_electronically_communtated_motor * input_less_than_500W
        * higher_output_or_airflow * meets_other_requirements)
