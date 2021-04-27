from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class motor_type(Enum):
    refrigeration = "Refrigeration"
    ventilation = "Ventilation"


class PDRS__motors__motor_type(Variable):
    entity = Building
    value_type = Enum
    possible_values = motor_type
    default_value = motor_type.refrigeration
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the motor type of your replacement, refrigeration or ventilation?"
    metadata = {
        'alias': "Motor Type",
        'variable-type': "input",
        "regulation_reference": PDRS_2022["X", "X.6"]
    }


class motor_poles_number(Enum):
    poles_2 = "poles_2"
    poles_4 = "poles_4"
    poles_6 = "poles_6"
    poles_8 = "poles_8"


class PDRS__motors__number_of_poles(Variable):
    entity = Building
    value_type = Enum
    possible_values = motor_poles_number
    default_value = motor_poles_number.poles_8
    definition_period = ETERNITY
    reference = "Clause **"
    label = "How many poles does your new motor have?"
    metadata = {
        'alias': "New Motor Poles Number ",
        'variable-type': "input",
        "regulation_reference": PDRS_2022["X", "X.6"]
    }
