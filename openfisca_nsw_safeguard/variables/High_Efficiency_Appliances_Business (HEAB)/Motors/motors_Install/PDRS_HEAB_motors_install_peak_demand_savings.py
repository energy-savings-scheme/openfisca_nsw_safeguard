from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class PDRS__motors_install_peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The Peak demand savings "
    metadata = {
        "variable-type": "output",
        "alias": "Motors Peak demand savings",
        "regulation_reference": PDRS_2022["XX", "motors"]
    }

    def formula(building, period, parameters):

        meets_all_requirements = building(
            'PDRS_motor_install_meets_all_requirements', period)
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
