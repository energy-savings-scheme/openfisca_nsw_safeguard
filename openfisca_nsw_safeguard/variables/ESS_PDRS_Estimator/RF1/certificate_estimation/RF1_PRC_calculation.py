from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

  
class RF1_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'RF2 PRC calculation'
    metadata = {
        'variable-type': 'output'
    }
    
    def formula(buildings, period, parameters):
        peak_demand_reduction_capacity = buildings('RF1_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('RF1_network_loss_factor', period) 
        storage_volume_eligibility = buildings('RF1_storage_volume', period)

        RF1_eligible_PRCs = np.select(
        [
            storage_volume_eligibility,
            np.logical_not(storage_volume_eligibility)
        ],
        [
            (peak_demand_reduction_capacity * network_loss_factor * 10),
            0
        ])

        result_to_return = np.select(
        [
            RF1_eligible_PRCs <= 0, RF1_eligible_PRCs > 0
        ],
        [
            0, RF1_eligible_PRCs
        ])
        return result_to_return