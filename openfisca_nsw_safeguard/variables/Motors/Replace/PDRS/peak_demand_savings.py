from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022
import numpy as np


class PDRS__motors__old_efficiency(Variable):
    entity = Building
    value_type = float
    default_value = -999
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the efficiency of your existing motor to be replaced , as found in the GEMS Registry?"
    metadata = {
        "variable-type": "input",
        "alias": "Efficiency (%) of The Old Motor",
        "regulation_reference": PDRS_2022["X", "X.6"]
    }


class PDRS__motors__existing_motor_efficiency(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the efficiency of your existing motor to be replaced , as found in the GEMS Registry?"
    metadata = {
        "variable-type": "intermediary",
        "alias": "Existing Motor Efficiency (use baseline efficiency if not supplied)",
        "regulation_reference": PDRS_2022["X", "X.6"]
    }

    def formula(building, period, paramters):
        old_efficiency = building('PDRS__motors__old_efficiency', period)
        baseline_efficiency = building(
            'PDRS__motors__baseline_motor_efficiency', period)
        return np.where(old_efficiency > 0, old_efficiency, baseline_efficiency)


class PDRS__motors__firmness_factor(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    metadata = {
        'alias': "Firmness Factor",
        'variable-type': "intermediary",
        "regulation_reference": PDRS_2022["X", "X.6"]
    }

    def formula(building, period, parameters):
        contribution_factor = parameters(
            period).PDRS.PDRS_wide_constants.CONTRIBUTION_FACTOR
        motor_type = building('motor_type_var', period)
        load_factor = parameters(
            period).PDRS.motors.motors_load_factor_table[motor_type]
        duration_factor = parameters(
            period).PDRS.motors.motors_duration_factor_table[motor_type]
        return duration_factor*load_factor*contribution_factor


class PDRS__motors__new_efficiency(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the efficiency of the new motor as %, as found in the GEMS Registry?"
    metadata = {
        "variable-type": "input",
        "alias": "Efficiency (%) of The New Motor",
        "regulation_reference": PDRS_2022["X", "X.6"]
    }


class PDRS__motors_replace_peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The Peak demand savings "
    metadata = {
        "variable-type": "output",
        "alias": "Motors Peak demand savings",
        "regulation_reference": PDRS_2022["X", "X.6"]
    }

    def formula(building, period, parameters):

        meets_all_requirements = building(
            'PDRS_replace_motors_meets_all_requirements', period)
        rated_output = building('motors_rated_output', period)
        new_efficiency = building('PDRS__motors__new_efficiency', period)
        existing_efficiency = building(
            'PDRS__motors__existing_motor_efficiency', period)
        firmness = building('PDRS__motors__firmness_factor', period)
        daily_window = parameters(
            period).PDRS.PDRS_wide_constants.DAILY_PEAK_WINDOW_HOURS
        asset_life_table = parameters(
            period).PDRS.motors.motors_asset_life_table
        forward_creation_period = asset_life_table.calc(
            rated_output, right=False)

        return meets_all_requirements * rated_output * (new_efficiency - existing_efficiency)/100 * firmness*daily_window * forward_creation_period
