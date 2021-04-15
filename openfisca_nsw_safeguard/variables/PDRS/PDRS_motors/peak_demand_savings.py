from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Building



class PDRS__motors__new_efficiency(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the efficiency of the new motor as %, as found in the GEMS Registry?"
    metadata={
        "variable-type": "input",
        "alias" :"Efficiency (%) of The New Motor",
        "activity-group":"High Efficiency Appliances for Business",
        "activity-name":"Replace a new high efficiency Motor (Refrigerations or Ventillations)"
        }


class PDRS__motors__new_motor_rated_output(Variable):
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
        rated_output = building('PDRS__motors__new_motor_rated_output', period)
        new_efficiency = building('PDRS__motors__new_efficiency', period)
        existing_efficiency = building('PDRS__motors__existing_motor_efficiency', period)
        firmness = building('PDRS__motors__firmness_factor', period)
        daily_window = parameters(period).PDRS.PDRS_wide_constants.DAILY_PEAK_WINDOW_HOURS
        asset_life_table=parameters(period).PDRS.motors.motors_asset_life_table
        forward_creation_period=asset_life_table.calc(rated_output, right=False)
       

        return rated_output * (new_efficiency - existing_efficiency)/100 * firmness*daily_window * forward_creation_period

