from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class PDRS_HEER_AC_replace_peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The final peak demand savings from the air conditioner"
    metadata = {
        "alias": "HEER AC Replace Peak Demand Savings",
        "regulation_reference": PDRS_2022["HEER", "AC_replace", "energy_savings"]
    }

    def formula(building, period, parameters):
        meets_all_requirements = building(
            "PDRS_HEER_AC_replace_meets_all_requirements", period)

        savings = building("PDRS_AC_peak_demand_savings", period)

        return meets_all_requirements*savings
