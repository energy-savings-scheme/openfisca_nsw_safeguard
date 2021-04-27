import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class PDRS_AC_replace_baseline_power_input(Variable):
    value_type = float
    entity = Building
    label = 'returns the baseline power input for an Air Conditioner'
    definition_period = ETERNITY
    metadata = {
        "variable-type": "intermediary",
        "alias": "Baseline Power Input",
        "regulation_reference": PDRS_2022["X", "X.5"]
    }

    def formula(building, period, parameters):
        cooling_capacity = building(
            'Air_Conditioner__cooling_capacity', period)

        cooling_capacity_enum = building('AC_cooling_capacity_enum', period)
        AC_type = building('Air_Conditioner_type', period)
        baseline_unit = parameters(
            period).PDRS.AC.AC_baseline_power_per_capacity_reference_table['replacement']
        scale = baseline_unit[AC_type]

        return scale[cooling_capacity_enum]*cooling_capacity


class PDRS_AC_replace_peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The final peak demand savings from the air conditioner"
    metadata = {
        "variable-type": "output",
        "alias": "AC Peak Demand Savings",
        "regulation_reference": PDRS_2022["X", "X.5"]
    }

    def formula(building, period, parameters):
        power_input = building('PDRS_AC_power_input', period)
        baseline_power_input = building(
            'PDRS_AC_replace_baseline_power_input', period)
        firmness_factor = building(
            'PDRS_AC_firmness_factor', period)
        daily_peak_hours = parameters(
            period).PDRS.PDRS_wide_constants.DAILY_PEAK_WINDOW_HOURS
        forward_creation_period = parameters(
            period).PDRS.AC.AC_related_constants.FORWARD_CREATION_PERIOD

        diff = np.where((baseline_power_input - power_input) >
                        0, baseline_power_input - power_input, 0)

        return diff*daily_peak_hours*firmness_factor*forward_creation_period
