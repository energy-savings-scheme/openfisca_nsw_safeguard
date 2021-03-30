from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class motor_type(Enum):
    refrigeration="Refrigeration"
    ventilation="Ventilation"


class PDRS__motors__motor_type(Variable):
    entity=Building
    value_type=Enum
    possible_values=motor_type
    default_value=motor_type.refrigeration
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the motor type of your replacement, refrigeration or ventilation?"
    metadata ={
        'alias' : "Motor Type",
        'activity-group' : "High Efficiency Appliances for Business",
        'activity-name' : "Replace an existing motor by a high efficiency motor",
        'variable-type' : "input"
    }


class PDRS__motors__firmness_factor(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    metadata ={
        'alias' : "Firmness Factor",
        'activity-group' : "High Efficiency Appliances for Business",
        'activity-name' : "Replace an existing motor by a high efficiency motor",
        'variable-type' : "intermediary"
    }

    def formula(building, period, parameters):
        contribution_factor = parameters(period).PDRS_wide_constants.CONTRIBUTION_FACTOR
        motor_type=building('PDRS__motors__motor_type', period)
        load_factor = parameters(period).motors.motors_load_factor_table[motor_type]
        duration_factor = parameters(period).motors.motors_duration_factor_table[motor_type]
        return duration_factor*load_factor*contribution_factor