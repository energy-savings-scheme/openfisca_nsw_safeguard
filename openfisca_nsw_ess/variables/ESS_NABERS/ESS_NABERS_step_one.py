from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY, YEAR
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

class ESS_NABERS_measured_electricity_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Measured Electricity Consumption (in MWh)"
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"Measured Electricity Consumption (MWh)",
        "major-cat":"Energy Savings Scheme",
        "monor-cat":'Metered Baseline Method - NABERS baseline'
        }

    def formula(buildings, period, parameters):
        return (buildings('ESS_NABERS_electricity', period)
        + buildings('ESS_NABERS_onsite_unaccounted_electricity', period))


class ESS_NABERS_electricity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8, Method 4 - Step 1"
    label = 'NABERS Electricity, in MWh, is the electricity purchased or' \
            ' imported from the Electricity Network and accounted for in the' \
            ' NABERS Rating, including electricity purchased as GreenPower.'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Electricity (MWh)",
        "major-cat":"Energy Savings Scheme",
        "monor-cat":'Metered Baseline Method - NABERS baseline'
        }


class ESS_NABERS_onsite_unaccounted_electricity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8, Method 4 - Step 1"
    label = 'What is the onsite unaccounted electricity use, that is not' \
            ' recorded on the NABERS Rating Report?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS On-site Unaccounted Electricity (MWh)",
        "major-cat":"Energy Savings Scheme",
        "monor-cat":'Metered Baseline Method - NABERS baseline'
        }


class ESS_NABERS_gas(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = 'NABERS Gas, in MWh, is the total of the Gas accounted for in' \
            ' the NABERS rating'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Gas (MWh)",
        "major-cat":"Energy Savings Scheme",
        "monor-cat":'Metered Baseline Method - NABERS baseline'
        }
