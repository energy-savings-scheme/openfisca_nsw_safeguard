from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022
from openfisca_nsw_safeguard.variables.ESS_general.ESS_BCA_climate_zone import BCA_climate_zone

import numpy as np

class PDRS_WH1_meets_equipment_requirements_air_source_heat_pump(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the installed end-user equipment an air source heat pump water heater as defined by AS/NZS 4234?'
    metadata = {
          'alias':  'air source heat pump water heater',
      }

# THIS VARIABLE IS NOT COMPLETED (Section 2): Need to define the HP3 / 5 etc zones that are used for modelling
class PDRS_WH1_meets_equipment_requirements_of_climate_zone(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the heat pump water heater achieve minimum annual energy savings?'
    metadata = {
        'alias':  'The heat pump water heater achieves minimum annual energy savings',
      }

    def formula(buildings, period, parameters):
        climate_zone = buildings('BCA_climate_zone', period)
        ESS_BCAClimateZone = (climate_zone.possible_values)
        is_ESS_BCA_climate_zone = (
                              (climate_zone == ESS_BCAClimateZone.BCA_Climate_Zone_1) +
                              (climate_zone == ESS_BCAClimateZone.BCA_Climate_Zone_2) +
                              (climate_zone == ESS_BCAClimateZone.BCA_Climate_Zone_3) +
                              (climate_zone == ESS_BCAClimateZone.BCA_Climate_Zone_4) +
                              (climate_zone == ESS_BCAClimateZone.BCA_Climate_Zone_5) +
                              (climate_zone == ESS_BCAClimateZone.BCA_Climate_Zone_6) +
                              (climate_zone == ESS_BCAClimateZone.BCA_Climate_Zone_7) +
                              (climate_zone == ESS_BCAClimateZone.BCA_Climate_Zone_8)
        )
        return is_ESS_BCA_climate_zone

class PDRS_WH1_meets_equipment_requirements_hot_water_pump_storage_volume(Variable):
    value_type = int
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the storage volume (in Litres) of your installed end-user equipment?'
    metadata = {
          'alias':  'Storage volume',
      }

class PDRS_WH1_meets_equipment_requirements_hot_water_pump_ASNZ_2712_certified(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is your equipment AS/NZ 2712 certified?'
    metadata = {
          'alias':  'AS/NZ 2712 certified'
      }

class PDRS_WH1_meets_equipment_requirements_storage_certified(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the end user equipment meet the storage and certification requirements for heat water pumps?'
    metadata = {
          'alias':  'AS/NZ 2712 certified'
      }

    def formula(buildings, period, parameters):
        heat_pump_storage_volume = buildings('PDRS_WH1_meets_equipment_requirements_hot_water_pump_storage_volume', period)
        is_ASNZ_2712_certified = buildings('PDRS_WH1_meets_equipment_requirements_hot_water_pump_ASNZ_2712_certified', period)
        storage_volume_less_than_700L = heat_pump_storage_volume < 700
        
        return (
            storage_volume_less_than_700L *
            is_ASNZ_2712_certified
        )

class PDRS_WH1_meets_equipment_requirements_administrator_approval(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Has the installed end user equipment been accepted by the Scheme Administrator?'
    metadata = {
        'alias' : 'Scheme Administrator approval'
    }
    
class PDRS_WH1_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the installed end-user equipment meet the Equipment Requirements?'
    metadata = {
        'alias':  'The installed end-user equipment meets the equipment requirements'
    }

    def formula(buildings, period, parameters):
        Air_source_heat_pump_water_heater = buildings('PDRS_WH1_meets_equipment_requirements_air_source_heat_pump', period)
        #Section 2 goes here
        Heat_pump_storage_certified = buildings('PDRS_WH1_meets_equipment_requirements_storage_certified', period)
        Administrator_approval = buildings('PDRS_WH1_meets_equipment_requirements_administrator_approval', period)
        climate_zone = buildings('BCA_climate_zone', period)
        ESS_BCAClimateZone = (climate_zone.possible_values)
        in_eligible_BCA_climate_zone = (np.logical_not(BCA_climate_zone == ESS_BCAClimateZone.BCA_Climate_Zone_1) + np.logical_not(BCA_climate_zone == ESS_BCAClimateZone.BCA_Climate_Zone_4))


        return (
                Air_source_heat_pump_water_heater *
                #Section 2
                Heat_pump_storage_certified * 
                Administrator_approval *
                in_eligible_BCA_climate_zone
                )
