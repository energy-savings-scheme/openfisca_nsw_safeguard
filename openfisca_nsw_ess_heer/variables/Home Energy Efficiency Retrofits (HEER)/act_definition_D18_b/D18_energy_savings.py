# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

class D18_b_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the deemed activity electricity savings for Activity' \
            ' Definition D18a (version with VEU registry integration)?'

    def formula(buildings, period, parameters):
        heat_pump_system_size = buildings('heat_pump_system_size', period)
        HeatPumpSystemSize = heat_pump_system_size.possible_values  # imports functionality of heat pump system size enum from user_inputs
        electricial_energy = buildings('D18_b_annual_electrical_energy', period)
        baseline_A = parameters(period).HEER.D18.table_D18_b_baseline_A_and_B.baseline_A[heat_pump_system_size]
        coefficient_b = parameters(period).HEER.D18.table_D18_b_coefficients.coefficient_b
        electricity_savings_factor = (baseline_A - coefficient_b * electricial_energy)
        return electricity_savings_factor


class D18_b_deemed_activity_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the deemed activity gas savings for Activity' \
            ' Definition D18a (version with VEU registry integration)?'

    def formula(buildings, period, parameters):
        heat_pump_system_size = buildings('heat_pump_system_size', period)
        HeatPumpSystemSize = heat_pump_system_size.possible_values  # imports functionality of heat pump system size enum from user_inputs
        supplementary_energy = buildings('D18_b_annual_supplementary_energy', period)
        baseline_B = parameters(period).HEER.D18.table_D18_b_baseline_A_and_B.baseline_B[heat_pump_system_size]
        coefficient_a = parameters(period).HEER.D18.table_D18_b_coefficients.coefficient_a
        gas_savings_factor = (baseline_B - coefficient_a * supplementary_energy)
        return gas_savings_factor


class D18_b_annual_supplementary_energy(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the annual supplementary energy used by the heat pump,' \
            ' measured in GJ?'


class D18_b_annual_electrical_energy(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the annual electrical energy used by the heat pump,' \
            ' measured in GJ?'
