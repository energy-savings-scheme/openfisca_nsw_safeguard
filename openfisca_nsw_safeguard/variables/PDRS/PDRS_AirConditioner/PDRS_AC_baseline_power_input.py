import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

class PDRS__Air_Conditioner__baseline_power_input(Variable):
    value_type = float
    entity = Building
    label = 'returns the baseline power input for an Air Conditioner'
    definition_period = ETERNITY
    metadata = {
        "variable-type": "intermediary",
        "alias": "Baseline Power Input",
        # "activity-group": "PDRS: Air Conditioner",
        # "activity-name": "Installation or Replacement of an Air Conditioner"
        "regulation_reference": PDRS_2022["8","5"]
    }

    def formula(building, period, parameters):
        cooling_capacity = building(
            'Air_Conditioner__cooling_capacity', period)

        cooling_capacity_enum = building('AC_cooling_capacity_enum', period)
        replace_or_new = building('Appliance__installation_type', period)
        AC_type = building('Air_Conditioner_type', period)
        baseline_unit = parameters(
            period).PDRS.AC.AC_baseline_power_per_capacity_reference_table[replace_or_new]
        scale = baseline_unit[AC_type]

        return scale[cooling_capacity_enum]*cooling_capacity
