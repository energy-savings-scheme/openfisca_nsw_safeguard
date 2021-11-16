from numpy.core.defchararray import _replace_dispatcher
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
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
        "regulation_reference": PDRS_2022["XX", "motors"]
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
        "regulation_reference": PDRS_2022["XX", "motors"]
    }

    def formula(building, period, paramters):
        install_or_replace = building('Appliance__installation_type', period)
        old_efficiency = building('PDRS__motors__old_efficiency', period)
        baseline_efficiency = building(
            'PDRS__motors__baseline_motor_efficiency', period)

        replace_baseline = np.where(
            old_efficiency > 0, old_efficiency, baseline_efficiency)
        # 0 is install, 1 is replacement
        return np.where(install_or_replace == 0, baseline_efficiency, replace_baseline)


class PDRS__motors__new_efficiency(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the efficiency of the new motor as %, as found in the GEMS Registry?"
    metadata = {
        "variable-type": "input",
        "alias": "Efficiency (%) of The New Motor",
        "regulation_reference": PDRS_2022["XX", "motors"]
    }


class PDRS_motors_peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The Peak demand savings "
    metadata = {
        "alias": "Motors Peak demand savings",
        "regulation_reference": PDRS_2022["XX", "motors"]
    }

    def formula(building, period, parameters):

        baseline_input_power = building('PDRS_install_motors_baseline_input_power', period)
        baseline_peak_load_adjustment_factor = (
        parameters(period).PDRS.table_A27_end_use_equipment_factors
        ['refrigeration_or_ventilation_motors']['baseline_peak_load_adjustment_factor']
        )
        input_power = building('PDRS_install_motors_power_input', period)
        peak_load_adjustment_factor = (
        parameters(period).PDRS.table_A27_end_use_equipment_factors
        ['refrigeration_or_ventilation_motors']['peak_load_adjustment_factor']
        )
        firmness_factor = (
        parameters(period).PDRS.table_A27_end_use_equipment_factors
        ['refrigeration_or_ventilation_motors']['firmness_factor']
        )

        return (
                (
                    baseline_input_power *
                    baseline_peak_load_adjustment_factor
                ) -
                (
                    input_power *
                    peak_load_adjustment_factor
                ) *
                firmness_factor
        )

class PDRS_install_motors_baseline_input_power(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "Calculate the power input for the install motors PDRS method. "
    metadata = {
        "alias": "Motors Peak demand savings",
        "regulation_reference": PDRS_2022["XX", "motors"]
    }

    def formula(buildings, period, parameters):
        rated_output = buildings('motors_rated_output', period)
        baseline_efficiency = buildings('PDRS__motors__existing_motor_efficiency', period)
        return (rated_output / baseline_efficiency)


class PDRS_install_motors_power_input(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "Calculate the power input for the install motors PDRS method. "
    metadata = {
        "alias": "Motors Peak demand savings",
        "regulation_reference": PDRS_2022["XX", "motors"]
    }

    def formula(buildings, period, parameters):
        rated_output = buildings('motors_rated_output', period)
        new_efficiency = buildings('PDRS__motors__new_efficiency', period)
        return (rated_output / new_efficiency)



