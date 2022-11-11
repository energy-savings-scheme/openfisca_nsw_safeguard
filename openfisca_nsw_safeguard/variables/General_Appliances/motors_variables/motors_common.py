from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class motor_type(Enum):
    refrigeration = "Refrigeration"
    ventilation = "Ventilation"


class motor_type_var(Variable):
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
        "regulation_reference": PDRS_2022["XX", "motors"]
    }


class motor_poles_number(Enum):
    poles_2 = "The motor is a 2 poles motor."
    poles_4 = "The motor is a 4 poles motor."
    poles_6 = "The motor is a 6 poles motor."
    poles_8 = "The motor is a 8 poles motor."


class motor_poles_number_var(Variable):
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
        "regulation_reference": PDRS_2022["XX", "motors"]
    }


class PDRS__motors__baseline_motor_efficiency(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "Baseline Motor Efficiency "
    metadata = {
        "variable-type": "intermediary",
        "alias": "Baseline Motor Efficiency",
        "regulation_reference": PDRS_2022["XX", "motors"]
    }

    def formula(building, period, parameters):
        rated_output = building('motors_rated_output', period)
        poles = building('motor_poles_number_var', period)

        node = parameters(period).PDRS.motors.motors_baseline_efficiency_50hz

        # Here we fetch value for each "pole_#" node
        # NOTE - this is a hacky workaround required because 'fancy indexing' doesn't work on SingleAmountTaxScales
        # See more at <https://openfisca.org/doc/coding-the-legislation/legislation_parameters#computing-a-parameter-that-depends-on-a-variable-fancy-indexing>

        # NOTE (Ram) - The `interpolate=True` keyword argument is functionality I've newly added to openfisca-core
        poles_2_value = node["poles_2"].rated_output.calc(
            rated_output, interpolate=True)
        poles_4_value = node["poles_4"].rated_output.calc(
            rated_output, interpolate=True)
        poles_6_value = node["poles_6"].rated_output.calc(
            rated_output, interpolate=True)
        poles_8_value = node["poles_8"].rated_output.calc(
            rated_output, interpolate=True)

        baseline_motor_efficiency = np.select([poles == motor_poles_number_var.possible_values.poles_2,
                                               poles == motor_poles_number_var.possible_values.poles_4,
                                               poles == motor_poles_number_var.possible_values.poles_6,
                                               poles == motor_poles_number_var.possible_values.poles_8,
                                               ],
                                              [poles_2_value, poles_4_value, poles_6_value, poles_8_value], 0)

        return baseline_motor_efficiency


class motor_registered_under_GEM(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the electric motor a registered product under GEMS?'
    metadata = {
        'alias':  'electric motor is a registered product under GEMS'
    }


class motor_3_phase_high_efficiency(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment a 3 phase electric motor rated "high efficiency"?'
    metadata = {
        'alias':  'electric motor is 3 phase high efficiency'
    }


class motors_rated_output(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the Rated Output of the old motor being replaced in kW as found in the GEMS Registry"
    metadata = {
        "variable-type": "input",
        "alias": "Rated Output of The New Motor",
        "regulation_reference": PDRS_2022["XX", "motors"]
    }
