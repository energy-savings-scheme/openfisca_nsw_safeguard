# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E6_hot_water_supply_service_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a 2 foot, 3 foot, 4 foot,' \
            ' or 5 foot T8 or T12 fluorescent reflector lamp, as required' \
            ' in Eligiblity Requirement 1 in Activity Definition E4,' \
            ' and defined in Table A9.1.'  # this light type is not defined anywhere in the rule (and probably should be!)

    def formula(buildings, period, parameters):
        hot_water_supply_service = buildings('hot_water_supply_service', period)
        is_electric_resistance = (hot_water_supply_service == HotWaterSupplyService.electric_resistance_water_heater)
        is_electric_boosted_solar = (hot_water_supply_service == HotWaterSupplyService.electric_boosted_solar_water_heater)
        is_electric_heat_pump = (hot_water_supply_service == HotWaterSupplyService.electric_heat_pump_water_heater)
        is_gas_fired_storage = (hot_water_supply_service == HotWaterSupplyService.gas_fired_storage_water_heater)
        is_gas_fired_instantaneous = (hot_water_supply_service == HotWaterSupplyService.gas_fired_instantaneous_water_heater)
        is_gas_boosted_solar = (hot_water_supply_service == HotWaterSupplyService.gas_boosted_solar_water_heater)
        return is_electric_resistance + is_electric_boosted_solar + is_electric_heat_pump + is_gas_fired_storage + is_gas_fired_instantaneous + is_gas_boosted_solar  # note addition is used to define "or" with booleans


class E6_shower_has_existing_showerhead(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the shower has an existing showerhead, as required' \
            ' in Eligibility Requirement 3 in Activity Definition E1.'  # insert definition requirements


class HotWaterSupplyService(Enum):
    electric_resistance_water_heater = 'An electric resistance water heater.'
    electric_boosted_solar_water_heater = 'An electrically boosted solar water heater.'
    electric_heat_pump_water_heater = 'An electric heat pump water heater.'
    gas_fired_storage_water_heater = 'A gas fired storage water heater.'
    gas_fired_instantaneous_water_heater = 'A gas fired instantaneous water heater.'
    gas_boosted_solar_water_heater = 'A gas boosted solar water heater.'


class hot_water_supply_service(Variable):
    value_type = Enum
    possible_values = HotWaterSupplyService
    default_value = HotWaterSupplyService.electric_resistance_water_heater
    entity = Building
    definition_period = ETERNITY
    label = 'Defines the type of hot water supply service used to supply a' \
            ' a replacement showerhead in Activity Definition E6.'
