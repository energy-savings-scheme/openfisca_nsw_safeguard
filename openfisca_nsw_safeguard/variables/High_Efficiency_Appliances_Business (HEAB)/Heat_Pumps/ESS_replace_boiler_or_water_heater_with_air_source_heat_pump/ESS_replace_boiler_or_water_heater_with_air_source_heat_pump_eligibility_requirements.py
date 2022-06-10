from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.variables.PDRS_activities.PDRS_WH1.PDRS_WH1_eligibility_requirements import PDRS_WH1_EquipmentTypes

import numpy as np

class ESS_replace_boiler_with_heat_pump_existing_equipment_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = PDRS_WH1_EquipmentTypes
    default_value = PDRS_WH1_EquipmentTypes.PDRS_WH1_Ineligible
    definition_period = ETERNITY
    label = 'What type of hot water equipment are you checking for eligibility?'
    metadata={
        "variable-type": "user-input",
        "alias":"WH1 Equipment Type",
        }


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_existing_equipment_is_eligible_type(Variable):
  value_type = bool
  entity = Building
  default_value = False
  definition_period = ETERNITY
  label = 'Is the new equipment an eligible type of equipment for Activity Definition F16?'

  def formula(buildings, period, parameters):
    equipment_type = buildings('ESS_replace_boiler_with_heat_pump_existing_equipment_type', period)
    ExistingEquipmentType = equipment_type.possible_values
    is_eligible_equipment_type = (
                            (equipment_type == ExistingEquipmentType.PDRS_WH1_Gas_Hot_Water_Heater) +
                            (equipment_type == ExistingEquipmentType.PDRS_WH1_Gas_Hot_Water_Boiler) +
                            (equipment_type == ExistingEquipmentType.PDRS_WH1_Electric_Hot_Water_Heater) +
                            (equipment_type == ExistingEquipmentType.PDRS_WH1_Electric_Hot_Water_Boiler)                                
    )
    return is_eligible_equipment_type


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_new_equipment_is_gas_boosted_air_sourced_heat_pump(Variable):
  value_type = bool
  entity = Building
  default_value = False
  definition_period = ETERNITY
  label = 'Is the new equipment an eligible type of equipment for Activity Definition F16?'


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_new_equipment_is_eligible_type_for_old_equipment(Variable):
  value_type = bool
  entity = Building
  default_value = False
  definition_period = ETERNITY
  label = 'Is the new equipment an eligible type of equipment for replacing the existing equipment?'

  def formula(buildings, period, parameters):
    existing_equipment_type = buildings(
        'ESS_replace_boiler_with_heat_pump_existing_equipment_type', period)
    new_equipment_is_gas_boosted = buildings(
        "ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_new_equipment_is_gas_boosted_air_sourced_heat_pump", period)
    ExistingEquipmentTypes = existing_equipment_type.possible_values
    return (
                (
                    (
                        (existing_equipment_type == ExistingEquipmentTypes.PDRS_WH1_Gas_Hot_Water_Heater) +
                        (existing_equipment_type == ExistingEquipmentTypes.PDRS_WH1_Gas_Hot_Water_Boiler)
                    ) *
                    new_equipment_is_gas_boosted
                ) +
                (
                    np.logical_not(existing_equipment_type == ExistingEquipmentTypes.PDRS_WH1_Gas_Hot_Water_Heater) +
                    np.logical_not(existing_equipment_type == ExistingEquipmentTypes.PDRS_WH1_Gas_Hot_Water_Heater)                       
                )
        )

class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_new_equipment_is_not_residential(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the building class for the Implementation not a residential building type?'
    metadata = {
        'alias': "HEAB AC install meets eligibility requirements",
    }



    def formula(buildings, period, parameters):
        BCA_building_class = buildings('BCA_building_class', period)
        BuildingClass = BCA_building_class.possible_values
        is_residential = (
                            (BCA_building_class == BuildingClass.BCA_Class_1a) +
                            (BCA_building_class == BuildingClass.BCA_Class_1b) +
                            (BCA_building_class == BuildingClass.BCA_Class_4)
        )
        return np.logical_not (is_residential)




class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the activity meet all of the Eligibility Requirements?'
    metadata = {
        'alias': "HEAB AC install meets eligibility requirements",
    }

    def formula(buildings, period, parameters):
        existing_equipment_is_eligible_type = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_existing_equipment_is_eligible_type', period)
        new_equipmnent_eligible_with_existing_equipment = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_new_equipment_is_eligible_type_for_old_equipment', period)
        not_residential_site = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_new_equipment_is_not_residential', period)

        return (
            existing_equipment_is_eligible_type *
            new_equipmnent_eligible_with_existing_equipment *
            not_residential_site   
        )