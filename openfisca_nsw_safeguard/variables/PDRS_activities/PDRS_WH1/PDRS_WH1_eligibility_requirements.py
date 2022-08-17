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
    equipment_type = buildings('WH1_EquipmentType', period)
    is_WH1_equipment_type = (
                            (equipment_type == PDRS_WH1_EquipmentTypes.PDRS_WH1_Electric_Hot_Water_Heater) +
                            (equipment_type == PDRS_WH1_EquipmentTypes.PDRS_WH1_Electric_Hot_Water_Boiler)                                
    )
    return is_WH1_equipment_type

class PDRS_WH1_EquipmentTypes(Enum):
   PDRS_WH1_Electric_Hot_Water_Boiler = 'Electric hot water boiler'
   PDRS_WH1_Electric_Hot_Water_Heater = 'Electric hot water heater'
   PDRS_WH1_Ineligible                = 'Ineligible hot water equipment' 

class WH1_EquipmentType(Variable):
    value_type = Enum
    entity = Building
    possible_values = PDRS_WH1_EquipmentTypes
    default_value = PDRS_WH1_EquipmentTypes.PDRS_WH1_Gas_Hot_Water_Heater
    definition_period = ETERNITY
    label = 'What type of hot water equipment are you checking for eligibility?'
    metadata={
        "variable-type": "user-input",
        "alias":"WH1 Equipment Type",
        }