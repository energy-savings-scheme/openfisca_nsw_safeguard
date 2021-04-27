from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

class PDRS__ROOA__peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The final peak demand savings from the air conditioner"
    metadata = {
        'alias': "Peak Demand Savings",
        'activity-group': "Removal Of Old Appliances",
        'activity-name': "Removal of a Spare Refrigerator or Freezer",
        'variable-type': "output",
        "regulation_reference": PDRS_2022["X","X.7"]
    }

    def formula(building, period, parameters):

        meet_all_requirements = building(
            'PDRS_ROOA_meets_all_requirements', period)
        average_summer_demand = parameters(
            period).PDRS.ROOA_fridge.ROOA_related_constants.AVERAGE_SUMMER_DEMAND
        firmness_factor = building('PDRS__ROOA__firmness_factor', period)
        daily_peak_hours = parameters(
            period).PDRS.PDRS_wide_constants.DAILY_PEAK_WINDOW_HOURS
        forward_creation_period = parameters(
            period).PDRS.ROOA_fridge.ROOA_related_constants.FORWARD_CREATION_PERIOD

        return meet_all_requirements * average_summer_demand*firmness_factor*daily_peak_hours*forward_creation_period
