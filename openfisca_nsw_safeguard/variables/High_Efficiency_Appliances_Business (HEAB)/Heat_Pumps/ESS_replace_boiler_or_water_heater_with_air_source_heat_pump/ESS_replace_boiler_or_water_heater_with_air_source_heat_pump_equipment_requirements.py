from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_meets_AS4234_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the installed end-user equipment an air source heat pump water heater as defined by AS/NZS 4234?'
    metadata = {
          'alias':  'air source heat pump water heater',
      }



# The installed End-User Equipment must achieve minimum annual energy savings, when determined as an air
# sourced heat pump in accordance with the modelling procedure Published by the Scheme Administrator, of:
# o 60% when modelled in climate zone HP3-AU if the Site is in BCA Climate Zone 2, 3, 4, 5 or 6;
# o 60% when modelled in climate zone HP5-AU if the Site is in BCA Climate Zone 7 or 8;

# in IPART's product registry, products can be modelled for both HP3-AU and HP5-AU.


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_has_minimum_energy_savings(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the energy savings of the heat pump, based on BCA Climate Zone?'
    metadata = {
          'alias':  'HP3 Climate Zone',
      }

    def formula(buildings, period, parameters):
        energy_savings = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_energy_savings', period)
        return (energy_savings >= 60)


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_energy_savings(Variable):
    value_type = float
    entity = Building
    default_value = 0
    definition_period = ETERNITY
    label = 'What is the energy savings of the heat pump, based on BCA Climate Zone?'
    metadata = {
          'alias':  'HP3 Climate Zone',
      }

    def formula(buildings, period, parameters):
        postcode = buildings('ESS__postcode', period)
        climate_zone = buildings('BCA_climate_zone', period)
        ClimateZone = climate_zone.possible_values

        HP3_energy_savings = buildings('ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_HP3_energy_savings', period)        
        HP5_energy_savings = buildings('ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_HP5_energy_savings', period)        

        energy_savings = np.select(
                [
                climate_zone == ClimateZone.BCA_Climate_Zone_1,
                (
                    (climate_zone == ClimateZone.BCA_Climate_Zone_2) +
                    (climate_zone == ClimateZone.BCA_Climate_Zone_3) +
                    (climate_zone == ClimateZone.BCA_Climate_Zone_4) +
                    (climate_zone == ClimateZone.BCA_Climate_Zone_5) +
                    (climate_zone == ClimateZone.BCA_Climate_Zone_6)
                ),
                (
                    (climate_zone == ClimateZone.BCA_Climate_Zone_7) +
                    (climate_zone == ClimateZone.BCA_Climate_Zone_8)
                )
        ],
        [
            0, 
            HP3_energy_savings,
            HP5_energy_savings
        ]
        )

        return energy_savings


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_HP3_energy_savings(Variable):
    value_type = float
    entity = Building
    default_value = 0
    definition_period = ETERNITY
    label = 'What is the energy savings of the heat pump, as modelled in climate zone HP3?'
    metadata = {
          'alias':  'HP3 Climate Zone',
      }


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_HP5_energy_savings(Variable):
    value_type = float
    entity = Building
    default_value = 0
    definition_period = ETERNITY
    label = 'What is the energy savings of the heat pump, as modelled in climate zone HP5?'
    metadata = {
          'alias':  'HP3 Climate Zone',
      }


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_storage_volume(Variable):
    value_type = int
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the storage volume (in Litres) of your installed end-user equipment?'
    metadata = {
          'alias':  'Storage volume',
      }

class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_ASNZ_2712_certified(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is your equipment AS/NZ 2712 certified?'
    metadata = {
          'alias':  'AS/NZ 2712 certified'
      }


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_storage_certified(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the end user equipment meet the storage and certification requirements for heat water pumps?'
    metadata = {
          'alias':  'AS/NZ 2712 certified'
      }

    def formula(buildings, period, parameters):
        heat_pump_storage_volume = buildings('ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_storage_volume', period)
        is_ASNZ_2712_certified = buildings('ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_ASNZ_2712_certified', period)
        storage_volume_less_than_700L = heat_pump_storage_volume < 700
        
        return (
            (
            storage_volume_less_than_700L *
            is_ASNZ_2712_certified
            ) +
            np.logical_not(storage_volume_less_than_700L)
        )


class ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the installed end-user equipment meet the Equipment Requirements?'
    metadata = {
        'alias':  'The installed end-user equipment meets the equipment requirements'
    }

    def formula(buildings, period, parameters):
        Air_source_heat_pump_water_heater = buildings('ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_meets_AS4234_requirements', period)
        #Section 2 goes here
        has_minimum_energy_savings = buildings(
            'ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_hot_water_pump_has_minimum_energy_savings', period)
        heat_pump_storage_certified = buildings('ESS_replace_boiler_or_water_heater_with_air_source_heat_pump_storage_certified', period)

        return (
                Air_source_heat_pump_water_heater *
                has_minimum_energy_savings *
                heat_pump_storage_certified 
                )
