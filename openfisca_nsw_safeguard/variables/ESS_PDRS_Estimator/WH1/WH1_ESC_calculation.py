from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class WH1_capacity_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Capacity Factor'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      HP_Cap = buildings('WH1_HP_capacity_factor', period)
      WH_Cap = buildings('WH1_WH_capacity_factor', period)

      capacity_factor = np.select(
                                 [
                                    (HP_Cap <= WH_Cap),
                                    (HP_Cap > WH_Cap)
                                 ],
                                 [
                                    1,
                                    WH_Cap / HP_Cap
                                 ]
                                 )

      return capacity_factor


class WH1_deemed_activity_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity gas savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      HP_gas = buildings('WH1_HP_gas', period)
      capacity_factor = buildings('WH1_capacity_factor', period)
      lifetime = parameters(period).ESS.HEAB.table_F16_1.lifetime

      gas_savings = -(HP_gas) * capacity_factor * [lifetime / 3.6]

      return gas_savings
