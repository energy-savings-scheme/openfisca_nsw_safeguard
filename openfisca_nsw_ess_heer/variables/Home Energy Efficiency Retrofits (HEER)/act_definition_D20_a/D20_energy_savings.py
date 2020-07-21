# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

class D20_a_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the deemed activity electricity savings for Activity' \
            ' Definition D20a (version with VEU registry integration)?'

    def formula(buildings, period, parameters):
        climate_zone = buildings('BCA_Climate_Zone', period)
        BCAClimateZone = climate_zone.possible_values  # imports functionality of climate zone enum from user_inputs
        HP_climate_zone = select([climate_zone == BCAClimateZone.BCA_Climate_Zones_2_and_3,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_4,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_5,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zone_6,
                                        climate_zone == BCAClimateZone.BCA_Climate_Zones_7_and_8],
                                       ["HP3_AU",
                                        "HP3_AU",
                                        "HP4_AU",
                                        "HP4_AU",
                                        "HP5_AU"])  # need to confirm mapping of BCA climate zones to HP climate zones
        heat_pump_system_size = buildings('heat_pump_system_size', period)
        HeatPumpSystemSize = heat_pump_system_size.possible_values  # imports functionality of heat pump system size enum from user_inputs
        supplementary_energy = buildings('D20_a_annual_supplementary_energy', period)
        electricial_energy = buildings('D20_a_annual_electrical_energy', period)
        baseline_A = parameters(period).HEER.D20.table_D20_a_baseline_A_and_B.baseline_A[heat_pump_system_size]
        coefficient_b = parameters(period).HEER.D20.table_D20_a_coefficient_b
        electricity_savings_factor = (baseline_A - coefficient_b * (supplementary_energy  + electricial_energy))
        return electricity_savings_factor


class D20_a_deemed_activity_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the deemed activity electricity savings for Activity' \
            ' Definition D20a (version with VEU registry integration)?'

    def formula(buildings, period, parameters):
        heat_pump_system_size = buildings('heat_pump_system_size', period)
        HeatPumpSystemSize = heat_pump_system_size.possible_values  # imports functionality of heat pump system size enum from user_inputs
        gas_savings = parameters(period).HEER.D20.table_D20_a_baseline_A_and_B.baseline_B[heat_pump_system_size]
        return gas_savings

class D20_a_annual_supplementary_energy(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the annual supplementary energy used by the heat pump,' \
            ' measured in GJ?'


class D20_a_annual_electrical_energy(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the annual electrical energy used by the heat pump,' \
            ' measured in GJ?'
