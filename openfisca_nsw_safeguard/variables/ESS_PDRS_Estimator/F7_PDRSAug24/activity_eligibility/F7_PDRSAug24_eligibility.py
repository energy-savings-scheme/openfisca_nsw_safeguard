from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class F7_PDRSAug24_installation_final_activity_eligibility(Variable):
    """
        Formula to calculate the SYS1 installation activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
       "variable-type": "output"
    }

    def formula(buildings, period, parameter):
      high_efficiency = buildings('F7_PDRSAug24_high_efficiency', period)
      registered_GEMS = buildings('F7_PDRSAug24_equipment_registered_in_GEMS', period)
      equipment_installed = buildings('F7_PDRSAug24_equipment_installed', period)
      ACP_engaged = buildings('F7_PDRSAug24_engaged_ACP', period)
      rated_output_eligible = buildings('F7_PDRSAug24_rated_output_eligible', period)

      end_formula = ( high_efficiency * registered_GEMS * equipment_installed
                     * ACP_engaged * rated_output_eligible )

      return end_formula