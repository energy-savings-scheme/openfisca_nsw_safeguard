import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022
from openfisca_nsw_safeguard.variables.General_Appliances.appliances_variables import installation_type


class PDRS_HEAB_AC_install_peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The final peak demand savings from the air conditioner"
    metadata = {
        "alias": "AC Peak Demand Savings",
        "regulation_reference": PDRS_2022["HEAB", "AC_install"]
    }

    def formula(building, period, parameters):
        meets_all_requirements = building(
            "PDRS_HEAB_AC_install_meets_implementation_requirements", period)

        power_input = building('PDRS_AC_power_input', period)
        baseline_power_input = building(
            'PDRS_AC_baseline_power_input', period)
        firmness_factor = building(
            'PDRS_AC_firmness_factor', period)
        daily_peak_hours = parameters(
            period).PDRS.PDRS_wide_constants.DAILY_PEAK_WINDOW_HOURS
        forward_creation_period = parameters(
            period).PDRS.AC.AC_related_constants.FORWARD_CREATION_PERIOD

        diff = np.where((baseline_power_input - power_input) >
                        0, baseline_power_input - power_input, 0)

        return meets_all_requirements*diff*daily_peak_hours*firmness_factor*forward_creation_period
