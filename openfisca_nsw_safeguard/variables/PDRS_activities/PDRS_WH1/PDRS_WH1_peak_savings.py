from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

class PDRS_WH1_peak_demand_savings(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = "The final peak demand savings from replacing or installing a new hot water heat pump"
   
    def formula(building, period, parameters):
        Baseline_Input_Power = building('Baseline_Input_Power', period)
        Baseline_Peak_Adjustment_Factor = building('Baseline_Peak_Adjustment_Factor', period)
        Peak_Adjustment_Factor = building('Peak_Adjustment_Factor', period)
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor.firmness_factor['WH1']
        Input_Power = building('Input_Power', period)

        return (
           (Baseline_Input_Power *
           Baseline_Peak_Adjustment_Factor -
           Input_Power *
           Peak_Adjustment_Factor) *
           firmness_factor
        )

class ComPkLoad(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = "Peak daily load in winter"

class Baseline_Input_Power(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = "Baseline input power"
   
    def formula(building, period, parameters):
        ComPkLoad = building('ComPkLoad', period)
        return 0.01 * ComPkLoad

class Baseline_Peak_Adjustment_Factor(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = "Baseline peak adjustment factor"

    def formula(building, period, parameters):
      baseline_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['baseline_peak_adjustment']['WH1']
      return (
        baseline_adjustment_factor
      )

class Peak_Adjustment_Factor(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = "Peak adjustment factor"

    def formula(building, period, parameters):
      peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['peak_adjustment']['WH1']
      return (
        peak_adjustment_factor
    )

class Annual_energy_savings(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = "Annual energy savings"

class Input_Power(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = "Input Power"

    def formula(building, period, parameters):
        Annual_energy_savings = building('Annual_energy_savings',period)
        Baseline_Input_Power = building('Baseline_Input_Power',period)
        return (
          (100 - Annual_energy_savings) *
          Baseline_Input_Power / 100
        )