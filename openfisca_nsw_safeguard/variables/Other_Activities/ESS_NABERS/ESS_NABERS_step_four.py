from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY, YEAR
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

import numpy as np

class ESS__NABERS_annual_electricity_savings(Variable):
    value_type = float
    default_value = 0
    entity = Building
    definition_period = ETERNITY
    label = 'Annual Electricity Savings (in MWh)'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"Annual Electricity Savings (MWh)",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8.8"]
        }

    def formula(buildings, period, parameters):
        type_of_creation = buildings('ESS__NABERS_type_of_creation', period)
        TypeOfCreation = (type_of_creation.possible_values)
        is_annually_created = (type_of_creation == TypeOfCreation.annual_creation)
        is_forward_created = (type_of_creation == TypeOfCreation.forward_creation)
        NABERS_electricity = buildings('ESS__NABERS_measured_electricity_consumption', period)
        benchmark_electricity = buildings('ESS__NABERS_benchmark_elec_consumption', period)
        regional_network_factor = buildings('ESS__regional_network_factor', period)
        counted_electricity_savings = buildings('ESS__NABERS_counted_electricity_savings', period)
        return (is_annually_created
                * (((benchmark_electricity - NABERS_electricity))
                * regional_network_factor
                - (counted_electricity_savings))
                * np.logical_not(is_forward_created))
        # need to build in previous year's electricity savings and logic around that


class ESS__NABERS_annual_gas_savings(Variable):
    value_type = float
    default_value = 0
    entity = Building
    definition_period = ETERNITY
    label = 'Annual Gas Savings (in MWh)'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"Annual Electricity Savings (MWh)",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8.8"]
        }

    def formula(buildings, period, parameters):
        type_of_creation = buildings('ESS__NABERS_type_of_creation', period)
        TypeOfCreation = (type_of_creation.possible_values)
        is_annually_created = (type_of_creation == TypeOfCreation.annual_creation)
        is_forward_created = (type_of_creation == TypeOfCreation.forward_creation)
        NABERS_gas = buildings('ESS__NABERS_measured_gas_consumption', period)
        benchmark_gas = buildings('ESS__NABERS_benchmark_gas_consumption', period)
        counted_gas_savings = buildings('ESS__NABERS_counted_gas_savings', period)
        return (is_annually_created
                * (((benchmark_electricity - NABERS_electricity))
                - (counted_electricity_savings))
                * np.logical_not(is_forward_created))


class ESS__NABERS_counted_electricity_savings(Variable):
    value_type = float
    default_value = 0
    entity = Building
    definition_period = ETERNITY
    label = 'Counted Electricity Savings (in MWh). These are the Electricity Savings' \
            ' for which savings have previously been created for.'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"Counted Electricity Savings (MWh)",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8.8"]
        }


class ESS__NABERS_counted_gas_savings(Variable):
    value_type = float
    default_value = 0
    entity = Building
    definition_period = ETERNITY
    label = 'Counted Gas Savings (in MWh). These are the Gas Savings' \
            ' for which savings have previously been created for.'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"Counted Gas Savings (MWh)",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8.8"]
        }
