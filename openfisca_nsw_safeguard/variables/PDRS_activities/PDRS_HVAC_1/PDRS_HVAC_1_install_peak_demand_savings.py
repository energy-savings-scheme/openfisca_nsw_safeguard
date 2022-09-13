from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

## detailed in PDRS activity XX

class PDRS_HVAC_1_install_peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The final peak demand savings from installing an air conditioner"
    metadata = {
        "alias": "AC Peak Demand Savings",
        "regulation_reference": PDRS_2022["HEAB", "AC_install", "energy_savings"]
    }

    def formula(building, period):
        meets_all_requirements = building(
            "PDRS_HVAC_1_install_meets_all_requirements", period)

        peak_capacity = building("PDRS_HVAC_1_peak_demand_saving_capacity", period)

        return meets_all_requirements*peak_capacity
