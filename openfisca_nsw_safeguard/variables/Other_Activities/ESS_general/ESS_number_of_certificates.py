from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS__electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the Electricity Savings created from an Implementation?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"ESS Electricity Savings",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Energy Savings Scheme - General'
        }

    def formula(buildings, period, parameters):
        ESS_method_type = buildings('ESS__method_type', period)
        ESS_MethodType = (ESS_method_type.possible_values)
        NABERS_electricity_savings = buildings('ESS__NABERS_electricity_savings', period)
        electricity_savings = np.select([ESS_method_type == (ESS_MethodType.clause_8_8_NABERS),
                                         ESS_method_type == (ESS_MethodType.clause_9_8_HEER)],
                                         [NABERS_electricity_savings,
                                          0])
        return electricity_savings
