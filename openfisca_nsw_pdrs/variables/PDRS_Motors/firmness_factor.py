from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class motor_type(Enum):
    refrigeration ="Motor is a refrigeration motor"
    ventilation ="Motor is a ventilation motor"


class PDRS__Motors_motor_type(Variable):
    entity=Building
    value_type=Enum
    possible_values=motor_type
    default_value=motor_type.refrigeration
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the type of motor?"
    metadata ={
        'alias' : "Zone Type",
        'activity-group' : "Motors?",
        'activity-name' : "Replace or Install an Motor",
        'variable-type' : "input"
    }
# maybe equipment_type is more appropriate?


class PDRS__motors__firmness_factor(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    metadata ={
        'alias' : "Firmness Factor",
        'activity-group' : "Removal Of Old Appliances",
        'activity-name' : "Removal of a Spare Refrigerator or Freezer",
        'variable-type' : "intermediary"
    }

    def formula(building, period, parameters):
        motor_type = building('PDRS__Motors_motor_type', period)
        contribution_factor = parameters(period).motors_related_constants.CONTRIBUTION_FACTOR
        duration_factor = parameters(period).motors_related_constants.DURATION_FACTOR[motor_type]
        load_factor = parameters(period).motors_load_factors_table[motor_type]
        return contribution_factor*load_factor*duration_factor
