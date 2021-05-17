import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022
from openfisca_nsw_safeguard.variables.General_Appliances.appliances_variables import installation_type


class PDRS_HEER_AC_install_peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The final peak demand savings from the air conditioner"
    metadata = {
        "variable-type": "output",
        "alias": "AC Peak Demand Savings",
        "regulation_reference": PDRS_2022["HEER", "AC_install", "energy_savings"]
    }

    def formula(building, period, parameters):
        meets_all_requirements = building(
            "PDRS_HEER_AC_install_meets_implementation_requirements", period)

        savings = building("PDRS_AC_peak_demand_savings", period)

        return meets_all_requirements*savings
