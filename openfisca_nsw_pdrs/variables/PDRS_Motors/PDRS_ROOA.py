from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class PDRS__motors__rated_output(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the rated output of the new motor, in kW, as found in the GEMS Registry?"
    metadata={"variable-type":"user_input"}


class PDRS__motors__new_efficiency(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the rated efficiency of the new motor, in %, as found in the GEMS Registry?"
    metadata={"variable-type":"user_input"}


class PDRS__motors__baseline_efficiency(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the rated efficiency of the old motor, in %, as found in the GEMS Registry?"
    metadata={"variable-type":"user_input"}


class PDRS__motors__peak_demand_savings(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="The final peak demand savings from the air conditioner"
    metadata ={
        'alias' : "Peak Demand Savings",
        'activity-group' : "Removal Of Old Appliances",
        'activity-name' : "Removal of a Spare Refrigerator or Freezer",
        'variable-type' : "output"
    }

    def formula(building, period, parameters):
        rated_output = building('PDRS__motors__rated_output', period)
        new_efficiency = building('PDRS__motors__new_efficiency', period)
        baseline_efficiency = building('PDRS__motors__baseline_efficiency', period)
        baseline_efficiency = where(baseline_efficiency == 0, (parameters(period).motors_rated_efficiency_table[number_of_poles]),
                                    baseline_efficiency)
        firmness_factor = building('PDRS__ROOA__firmness_factor', period)
        daily_peak_hours = parameters(period).ROOA_related_constants.DAILY_PEAK_WINDOW_HOURS
        forward_creation_period=parameters(period).ROOA_related_constants.FORWARD_CREATION_PERIOD


        return average_summer_demand*firmness_factor*daily_peak_hours*forward_creation_period
