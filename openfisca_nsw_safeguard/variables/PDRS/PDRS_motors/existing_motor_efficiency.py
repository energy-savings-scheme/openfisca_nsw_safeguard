import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_core.parameters import load_parameter_file

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

class motor_poles_number(Enum):
    poles_2="poles_2"
    poles_4="poles_4"
    poles_6="poles_6"
    poles_8="poles_8"



class PDRS__motors__number_of_poles(Variable):
    entity=Building
    value_type=Enum
    possible_values=motor_poles_number
    default_value=motor_poles_number.poles_8
    definition_period=ETERNITY
    reference="Clause **"
    label="How many poles does your new motor have?"
    metadata ={
        'alias' : "New Motor Poles Number ",
        # 'activity-group' : "High Efficiency Appliances for Business",
        # 'activity-name' : "Replace an existing motor by a high efficiency motor",
        'variable-type' : "input",
        "regulation_reference": PDRS_2022["8","5"]
    }



class PDRS__motors__old_efficiency(Variable):
    entity=Building
    value_type=float
    default_value = -999
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the efficiency of your existing motor to be replaced , as found in the GEMS Registry?"
    metadata={
        "variable-type": "input",
        "alias" :"Efficiency (%) of The Old Motor",
        # "activity-group":"High Efficiency Appliances for Business",
        # "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
        "regulation_reference": PDRS_2022["8","5"]
        }


class PDRS__motors__baseline_motor_efficiency(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="Baseline Motor Efficiency "
    metadata={
        "variable-type": "intermediary",
        "alias" :"Baseline Motor Efficiency",
        # "activity-group":"High Efficiency Appliances for Business",
        # "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
        "regulation_reference": PDRS_2022["8","5"]
        }

    def formula(building, period, parameters):
        rated_output = building('PDRS__motors__new_motor_rated_output', period)
        poles = building('PDRS__motors__number_of_poles', period)

        node = parameters(period).PDRS.motors.motors_baseline_efficiency_table

        # Here we fetch value for each "pole_#" node
        # NOTE - this is a hacky workaround required because 'fancy indexing' doesn't work on SingleAmountTaxScales
        # See more at <https://openfisca.org/doc/coding-the-legislation/legislation_parameters#computing-a-parameter-that-depends-on-a-variable-fancy-indexing>

        # NOTE (Ram) - The `interpolate=True` keyword argument is functionality I've newly added to openfisca-core
        poles_2_value = node["poles_2"].rated_output.calc(rated_output, interpolate=True)
        poles_4_value = node["poles_4"].rated_output.calc(rated_output, interpolate=True)
        poles_6_value = node["poles_6"].rated_output.calc(rated_output, interpolate=True)
        poles_8_value = node["poles_8"].rated_output.calc(rated_output, interpolate=True)

        baseline_motor_efficiency = np.select([poles == PDRS__motors__number_of_poles.possible_values.poles_2,
                          poles == PDRS__motors__number_of_poles.possible_values.poles_4,
                          poles == PDRS__motors__number_of_poles.possible_values.poles_6,
                          poles == PDRS__motors__number_of_poles.possible_values.poles_8,
                         ],
                         [poles_2_value, poles_4_value, poles_6_value, poles_8_value], 0)

        return baseline_motor_efficiency


class PDRS__motors__existing_motor_efficiency(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the efficiency of your existing motor to be replaced , as found in the GEMS Registry?"
    metadata={
        "variable-type": "intermediary",
        "alias" :"Existing Motor Efficiency (baseline efficiency if not supplied)",
        # "activity-group":"High Efficiency Appliances for Business",
        # "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
        "regulation_reference": PDRS_2022["8","5"]
        }

    def formula(building, period, paramters):
        old_efficiency = building('PDRS__motors__old_efficiency', period)
        baseline_efficiency = building('PDRS__motors__baseline_motor_efficiency', period)
        return np.where(old_efficiency>0, old_efficiency, baseline_efficiency)