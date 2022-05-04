from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

class PDRS_WH1_meets_equipment_requirements(Variable):
  value_type = bool
  entity = Building
  default_value = False
  definition_period = ETERNITY
  label = 'Does the implementation meet all of the Eligibility' \
          ' Requirements defined in Removal of Old Appliance (Heat pump water heater)?'
