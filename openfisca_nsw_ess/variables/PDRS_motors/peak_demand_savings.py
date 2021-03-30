import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class PDRS__motors__rated_output(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the Rated Output of the old motor being replaced in kW as found in the GEMS Registry"
    metadata={
        "variable-type": "input",
        "alias" :"Rated Output of The New Motor",
        "activity-group":"High Efficiency Appliances for Business",
        "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
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
        "activity-group":"High Efficiency Appliances for Business",
        "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
        }

    def formula(building, period, parameters):
        rated_output = building('PDRS__motors__rated_output', period)

        baseline_efficiency_table=parameters(period).motors.motors_baseline_efficiency_table
        return baseline_efficiency_table.calc(rated_output, right=False)



class PDRS__motors__peak_demand_savings(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="The Peak demand savings "
    metadata={
        "variable-type": "output",
        "alias" :"Motors Peak demand savings",
        "activity-group":"High Efficiency Appliances for Business",
        "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
        }

    def formula(building, period, parameters):
        rated_output = building('PDRS__motors__rated_output', period)
        print(rated_output)
        asset_life_table=parameters(period).motors.motors_asset_life_table
        forward_creation_period=asset_life_table.calc(rated_output, right=False)

        return forward_creation_period