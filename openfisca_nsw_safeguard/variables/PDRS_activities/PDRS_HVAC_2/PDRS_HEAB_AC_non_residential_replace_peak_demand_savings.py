from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

## detailed in PDRS activity XX

class PDRS_HEAB_non_residential_AC_replace_peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The final peak demand savings from replacing an air conditioner"
    metadata = {
        "alias": "HEAB AC (replace) Peak Demand Savings",
        "regulation_reference": PDRS_2022["HEAB", "AC_replace", "energy_savings"]
    }

    def formula(building, period, parameters):
        meets_all_requirements = building(
            "PDRS_HEAB_non_residential_AC_replace_meets_all_requirements", period)

        savings = building("PDRS_AC_peak_demand_savings", period)

        return meets_all_requirements*savings
