# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

class D16_a_is_listed_on_product_register(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment listed on a product register?'


class D16_a_is_certified_to_AS_NZS_2712(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment certified to the standard of AS/NZS' \
            ' 2712?'


class certified_to_60_percent_savings_in_zone_HP5_AU(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment certified to the standard of AS/NZS' \
            ' 2712?'
    # need to figure out logic for climate zones


class meets_VEU_ESC_product_application_guide_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product meet the requirements detailed in the Essential' \
            ' Services Commission Water Heating and Space Heating/Cooling' \
            ' Product Application Guide (C/18/24089)?'
    # long term idea. You could probably build in a flag to the product register \
    # requirement that asks whether it's registered within the VEU registry - \
    # and if that flag is true, require this to be true
    # is the intent for this only to apply to pumps installed in HP3-AU?

class D16_a_meets_all_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the equipment requirements detailed' \
            ' in Activity Definition F16 - version A?'

    def formula(buildings, period, parameters):
        listed_on_product_register = buildings('D16_a_is_listed_on_product_register', period)
        product_is_certified_to_standard = buildings('D16_a_is_certified_to_AS_NZS_2712', period)
        climate_zone = buildings('BCA_Climate_Zone', period)
        BCAClimateZone = climate_zone.possible_values  # imports functionality of climate zone enum from user_inputs
        in_climate_zone_7_and_8 = (climate_zone == BCAClimateZone.BCA_Climate_Zones_7_and_8)
        certified_to_60_percent_savings = buildings('certified_to_60_percent_savings_in_zone_HP5_AU', period)
        meets_minimum_savings_if_required = ((in_climate_zone_7_and_8 * certified_to_60_percent_savings)
        + (not(in_climate_zone_7_and_8)))
        meets_VEU_product_requirements = buildings('meets_VEU_ESC_product_application_guide_requirements', period)
        return (listed_on_product_register * product_is_certified_to_standard
        * meets_minimum_savings_if_required * meets_VEU_product_requirements)
