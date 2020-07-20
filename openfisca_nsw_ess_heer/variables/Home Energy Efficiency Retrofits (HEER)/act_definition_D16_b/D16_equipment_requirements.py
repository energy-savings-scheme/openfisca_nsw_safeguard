# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

class D16_b_is_listed_on_product_register(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment listed on a product register?'


class D16_b_is_certified_to_AS_NZS_2712(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment certified to the standard of AS/NZS' \
            ' 2712?'


class D16_b_certified_to_60_percent_savings_in_zone_HP5_AU(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment certified to have performance of at least 60%' \
            ' savings in climate zone HP5_AU?'
    # need to figure out logic for climate zones


class D16_b_certified_to_60_percent_savings_in_zone_HP3_AU(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment certified to have performance of at least 60%' \
            ' savings in climate zone HP5_AU?'
    # need to figure out logic for climate zones


class D16_b_meets_all_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the equipment requirements detailed' \
            ' in Activity Definition F16 - version A?'

    def formula(buildings, period, parameters):
        listed_on_product_register = buildings('D16_b_is_listed_on_product_register', period)
        product_is_certified_to_standard = buildings('D16_b_is_certified_to_AS_NZS_2712', period)
        climate_zone = buildings('BCA_Climate_Zone', period)
        BCAClimateZone = climate_zone.possible_values  # imports functionality of climate zone enum from user_inputs
        in_climate_zone_7_and_8 = (climate_zone == BCAClimateZone.BCA_Climate_Zones_7_and_8)
        in_climate_zone_2_and_3 = (climate_zone == BCAClimateZone.BCA_Climate_Zones_2_and_3)
        certified_to_60_percent_savings_in_HP5 = buildings('certified_to_60_percent_savings_in_zone_HP5_AU', period)
        certified_to_60_percent_savings_in_HP3 = buildings('certified_to_60_percent_savings_in_zone_HP3_AU', period)
        meets_minimum_savings_in_HP5 = ((in_climate_zone_7_and_8 * certified_to_60_percent_savings_in_HP5)
        + (not(in_climate_zone_7_and_8)))
        meets_minimum_savings_in_HP3 = ((in_climate_zone_2_and_3 * certified_to_60_percent_savings_in_HP3)
        + (not(in_climate_zone_2_and_3)))
        return (listed_on_product_register * product_is_certified_to_standard
        * meets_minimum_savings_in_HP5 * meets_minimum_savings_in_HP3)
