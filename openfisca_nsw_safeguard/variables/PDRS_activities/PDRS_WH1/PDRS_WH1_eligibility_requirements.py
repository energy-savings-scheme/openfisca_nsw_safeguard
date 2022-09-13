from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

class PDRS_WH1_meets_eligibility_requirements(Variable):
  value_type = bool
  entity = Building
  default_value = False
  definition_period = ETERNITY
  label = 'Does the implementation meet all of the Eligibility' \
          ' Requirements defined in Removal of Old Appliance (Heat pump water heater)?'

  def formula(buildings, period, parameters):
    equipment_type = buildings('gas_heater_equipment_type', period)
    is_WH1_equipment_type = (
                            (equipment_type == GasHeaterEquipmentTypes.Electric_Hot_Water_Heater) +
                            (equipment_type == GasHeaterEquipmentTypes.Electric_Hot_Water_Boiler)                                
    )
    return is_WH1_equipment_type

class GasHeaterEquipmentTypes(Enum):
   Gas_Hot_Water_Heater = 'Gas hot water heater.'
   Gas_Hot_Water_Boiler = 'Gas hot water boiler.'
   Electric_Hot_Water_Boiler = 'Electric hot water boiler'
   Electric_Hot_Water_Heater = 'Electric hot water heater'
   Ineligible                = 'Ineligible hot water equipment' 

#Kate let's keep this as one list to use in both ESS and PDRS methods, and then reduce
#eligibility for PDRS activity within eligibility requirements variable above
#we shouldn't have two lists of possible gas heaters


class gas_heater_equipment_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = GasHeaterEquipmentTypes
    default_value = GasHeaterEquipmentTypes.Electric_Hot_Water_Heater
    definition_period = ETERNITY
    label = 'What type of hot water equipment are you checking for eligibility?'
    metadata={
        "variable-type": "user-input",
        "alias":"WH1 Equipment Type",
        }