from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class PDRS_ROOA_firmness_factor(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    metadata = {
        'alias': "ROOA Refrigerator Firmness Factor",
    }

    def formula(building, period, parameters):
        load_factor = parameters(
            period).PDRS.ROOA_fridge.ROOA_related_constants.LOAD_FACTOR
        contribution_factor = parameters(
            period).PDRS.PDRS_wide_constants.CONTRIBUTION_FACTOR
        duration_factor = parameters(
            period).PDRS.ROOA_fridge.ROOA_related_constants.DURATION_FACTOR
        return contribution_factor*load_factor*duration_factor


class PDRS_ROOA_fridge_peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The final peak demand savings from the air conditioner"
    metadata = {
        'alias': "PDRS ROOA Spare Fridge Peak Demand Savings",
        "regulation_reference": PDRS_2022["ROOA", "fridge", "energy_savings"]
    }

    def formula(buildings, period, parameters):

        meet_all_requirements = buildings(
            'PDRS_ROOA_meets_all_requirements', period)
        baseline_input_power = (
            parameters(period).PDRS.ROOA_fridge.ROOA_related_constants
            ['baseline_input_power']
            )
        baseline_peak_load_adjustment_factors = (
            parameters(period).PDRS.table_A4_adjustment_factors['baseline_peak_adjustment']['RF1']
            )
        input_power = 0
        peak_load_adjustment_factor = baseline_peak_load_adjustment_factors
        firmness_factor = (
            parameters(period).PDRS.table_A6_firmness_factor['firmness_factor']['RF1']
            )
        return (
                meet_all_requirements * 
                (
                    (
                        (
                            baseline_input_power *
                            baseline_peak_load_adjustment_factors
                        ) -
                        (
                            input_power *
                            peak_load_adjustment_factor
                        )
                    ) *
                    firmness_factor
                )
            )