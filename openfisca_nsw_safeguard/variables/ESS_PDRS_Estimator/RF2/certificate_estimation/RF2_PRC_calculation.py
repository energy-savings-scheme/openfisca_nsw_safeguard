from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class RF2_baseline_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      total_energy_consumption = buildings('RF2_total_energy_consumption', period)
      af = buildings('RF2_af', period)
      baseline_EEI = buildings('RF2_baseline_EEI', period)
      product_EEI = buildings('RF2_product_EEI', period)
      
      baseline_input_power = np.multiply((total_energy_consumption * af), (baseline_EEI / product_EEI) / 24)
      return baseline_input_power
  
  
class RF2_peak_demand_savings_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      baseline_peak_adjustment_factor = buildings('RF2_baseline_peak_adjustment_factor', period)
      baseline_input_power = buildings('RF2_baseline_input_power', period)
      input_power = buildings('RF2_input_power', period)
      firmness_factor = 1

      peak_demand_savings_capacity= ((baseline_peak_adjustment_factor * baseline_input_power)
                                        - (input_power * baseline_peak_adjustment_factor )) * firmness_factor
      return peak_demand_savings_capacity
  
  
class RF2_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      peak_demand_savings_capacity = buildings('RF2_peak_demand_savings_capacity', period)
      summer_peak_demand_reduction_duration = 6
      lifetime = buildings('RF2_lifetime_by_rc_class', period)

      return peak_demand_savings_capacity * summer_peak_demand_reduction_duration * lifetime


class RF2_baseline_peak_adjustment_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Adjustment Factor'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
      product_type = buildings('RF2_product_type', period)
      duty_type = buildings('RF2_duty_class', period)
      usage_factor = 1
      
      temperature_factor = parameters(period).PDRS.refrigerated_cabinets.table_RF2_2['temperature_factor'][product_type][duty_type]
        # 1.14
      baseline_peak_adjustment_factor = temperature_factor * usage_factor
      return baseline_peak_adjustment_factor
  
  
class RF2_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'label' : 'The number of PRCs for RF2',
        'variable-type' : 'output'
    }

    def formula(buildings, period, parameters):
        peak_demand_capacity = buildings('RF2_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('RF2_network_loss_factor', period)
        kw_to_0_1kw = 10
        replacement_activity = buildings('RF2_replacement_activity', period)
        EEI_eligible_replacement = buildings('RF2_product_EEI_PRC_replacement_eligibility', period)
        EEI_eligible_install = buildings('RF2_product_EEI_ESC_install_eligibility', period)

        RF2_eligible_PRCs = np.select(
            [
                replacement_activity * EEI_eligible_replacement,
                np.logical_not(replacement_activity) * np.logical_not(EEI_eligible_replacement),
                replacement_activity * EEI_eligible_install,
                np.logical_not(replacement_activity) * EEI_eligible_install
            ],
            [
                (peak_demand_capacity * network_loss_factor * kw_to_0_1kw),
                0,
                0,
                0
            ])

        result_to_return = np.select(
            [
                RF2_eligible_PRCs <= 0, RF2_eligible_PRCs > 0
            ],
            [
                0, RF2_eligible_PRCs
            ])
        print('replacement activity', replacement_activity)
        print('eligible replacement', EEI_eligible_replacement)
        print('eligible install', EEI_eligible_install)
        print('PRCs', RF2_eligible_PRCs)
        return result_to_return