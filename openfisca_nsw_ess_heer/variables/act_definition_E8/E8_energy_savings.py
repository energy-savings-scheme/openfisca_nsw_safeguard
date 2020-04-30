# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E8_residential_electricity_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('E8_warranty_length', period)
        warranty_period = select([warranty_length <= 5, warranty_length > 5],
                                 ["two_to_five_year_warranty", "over_five_year_warranty"])
        climate_zone = buildings('BCA_Climate_Zone', period)
        BCAClimateZone = climate_zone.possible_values  # imports functionality of climate zone enum from user_inputs
        activity_climate_zone = select ([climate_zone == BCAClimateZone.BCA_Climate_Zones_2_and_3,
                                         climate_zone == BCAClimateZone.BCA_Climate_Zone_4,
                                         climate_zone == BCAClimateZone.BCA_Climate_Zone_5,
                                         climate_zone == BCAClimateZone.BCA_Climate_Zone_6,
                                         climate_zone == BCAClimateZone.BCA_Climate_Zones_7_and_8],
                                        ["climate_zones_2_and_3",
                                         "climate_zone_4",
                                         "climate_zone_5",
                                         "climate_zone_6",
                                         "climate_zones_7_and_8"])
        residential_electricity_savings_factor = parameters(period).table_E8_1.residential_electricity_savings_factor[warranty_period][activity_climate_zone]
        return residential_electricity_savings_factor


class E8_residential_gas_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('E8_warranty_length', period)
        warranty_period = select([warranty_length <= 5, warranty_length > 5],
                                 ["two_to_five_year_warranty", "over_five_year_warranty"])
        climate_zone = buildings('BCA_Climate_Zone', period)
        BCAClimateZone = climate_zone.possible_values  # imports functionality of climate zone enum from user_inputs
        activity_climate_zone = select ([climate_zone == BCAClimateZone.BCA_Climate_Zones_2_and_3,
                                         climate_zone == BCAClimateZone.BCA_Climate_Zone_4,
                                         climate_zone == BCAClimateZone.BCA_Climate_Zone_5,
                                         climate_zone == BCAClimateZone.BCA_Climate_Zone_6,
                                         climate_zone == BCAClimateZone.BCA_Climate_Zones_7_and_8],
                                        ["climate_zones_2_and_3",
                                         "climate_zone_4",
                                         "climate_zone_5",
                                         "climate_zone_6",
                                         "climate_zones_7_and_8"])
        residential_gas_savings_factor = parameters(period).table_E8_2.residential_gas_savings_factor[warranty_period][activity_climate_zone]
        return residential_gas_savings_factor
