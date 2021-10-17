from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Building


class new_motor_nominal_input_power(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What is the nominal input power of the new motor?'


class existing_motor_equipment_output_power(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What is the output power of the existing motor?'


class new_motor_equipment_output_power(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What is the output power of the new motor?'


class existing_motor_equipment_airflow_volume(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What is the airflow volume of the existing motor?'


class new_motor_equipment_airflow_volume(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What is the airflow volume of the new motor?'
