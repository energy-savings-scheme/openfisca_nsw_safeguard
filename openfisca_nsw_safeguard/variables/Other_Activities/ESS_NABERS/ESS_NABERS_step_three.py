from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY, YEAR
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021


class ESS__NABERS_benchmark_elec_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Benchmark Electricity Consumption (in MWh) - this is the value returned' \
            ' from the NABERS Reverse Calculator to achieve the Benchmark NABERS Rating' \
            ' over the Rating Period, using the same breakdown of energy consumption' \
            ' and the same input variables.'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"Benchmark Electricity Consumption (MWh)",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8.8"]
        }


class ESS__NABERS_benchmark_gas_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Benchmark Gas Consumption (in MWh) - this is the value returned' \
            ' from the NABERS Reverse Calculator to achieve the Benchmark NABERS Rating' \
            ' over the Rating Period, using the same breakdown of energy consumption' \
            ' and the same input variables.'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"Benchmark Gas Consumption (MWh)",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8.8"]
        }
