from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Building
import numpy as np

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022
from openfisca_nsw_safeguard.variables.Motors.motors_variables import PDRS__motors__number_of_poles


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


class PDRS__motors__baseline_motor_efficiency(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "Baseline Motor Efficiency "
    metadata = {
        "variable-type": "intermediary",
        "alias": "Baseline Motor Efficiency",
        "regulation_reference": PDRS_2022["X", "X.6"]
    }

    def formula(building, period, parameters):
        rated_output = building('PDRS__motors__new_motor_rated_output', period)
        poles = building('PDRS__motors__number_of_poles', period)

        node = parameters(period).PDRS.motors.motors_baseline_efficiency_table

        # Here we fetch value for each "pole_#" node
        # NOTE - this is a hacky workaround required because 'fancy indexing' doesn't work on SingleAmountTaxScales
        # See more at <https://openfisca.org/doc/coding-the-legislation/legislation_parameters#computing-a-parameter-that-depends-on-a-variable-fancy-indexing>

        # NOTE (Ram) - The `interpolate=True` keyword argument is functionality I've newly added to openfisca-core
        poles_2_value = node["poles_2"].rated_output.calc(
            rated_output, interpolate=True)
        poles_4_value = node["poles_4"].rated_output.calc(
            rated_output, interpolate=True)
        poles_6_value = node["poles_6"].rated_output.calc(
            rated_output, interpolate=True)
        poles_8_value = node["poles_8"].rated_output.calc(
            rated_output, interpolate=True)

        baseline_motor_efficiency = np.select([poles == PDRS__motors__number_of_poles.possible_values.poles_2,
                                               poles == PDRS__motors__number_of_poles.possible_values.poles_4,
                                               poles == PDRS__motors__number_of_poles.possible_values.poles_6,
                                               poles == PDRS__motors__number_of_poles.possible_values.poles_8,
                                               ],
                                              [poles_2_value, poles_4_value, poles_6_value, poles_8_value], 0)

        return baseline_motor_efficiency


class PDRS__motors__existing_motor_efficiency(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the efficiency of your existing motor to be replaced , as found in the GEMS Registry?"
    metadata = {
        "variable-type": "intermediary",
        "alias": "Existing Motor Efficiency (baseline efficiency if not supplied)",
        "regulation_reference": PDRS_2022["X", "X.6"]
    }

    def formula(building, period, paramters):
        old_efficiency = building('PDRS__motors__old_efficiency', period)
        baseline_efficiency = building(
            'PDRS__motors__baseline_motor_efficiency', period)
        return np.where(old_efficiency > 0, old_efficiency, baseline_efficiency)


class PDRS_replace_motors_meets_all_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the' \
            ' Requirements defined in PDRS replace or install high efficiency motors activity?'
    metadata = {
        'alias': "Replacement motor meets all requirements",
        "regulation_reference": PDRS_2022["X", "X.6"]
    }

    def formula(buildings, period, parameters):
        implementation = buildings(
            'PDRS_replace_motors_meets_implementation_requirements', period)
        return implementation


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
        motor_type = building('PDRS__motors__motor_type', period)
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


class PDRS__motors__new_motor_rated_output(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the Rated Output of the old motor being replaced in kW as found in the GEMS Registry"
    metadata = {
        "variable-type": "input",
        "alias": "Rated Output of The New Motor",
        "regulation_reference": PDRS_2022["X", "X.6"]
    }


class PDRS__motors__peak_demand_savings(Variable):
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
        rated_output = building('PDRS__motors__new_motor_rated_output', period)
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
