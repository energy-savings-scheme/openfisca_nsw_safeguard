from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_HEER_replace_halogen_floodlight_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the electricity savings for activity definition E1.'

    def formula(buildings, period, parameters):
        site_type = buildings('ESS_site_type', period)
        ESS_SiteType = site_type.possible_values

        is_residential = (site_type == ESS_SiteType.residential)
        is_small_business = (site_type == ESS_SiteType.small_business)

        electricity_savings = np.select(
                [is_residential,
                is_small_business,
                np.logical_not(is_residential + is_small_business)
                ],
                [
                        buildings('ESS_HEER_replace_halogen_floodlight_residential_savings_factor', period),
                        buildings('ESS_HEER_replace_halogen_floodlight_small_business_savings_factor', period),
                        0
                ]
                )

        return electricity_savings


class ESS_HEER_replace_halogen_floodlight_residential_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        existing_lamp_LCP = buildings('ESS_HEER_lighting_existing_lamp_circuit_power', period)
        LCP_of_existing_lamp = np.select(
                                        [
                                        (existing_lamp_LCP < 100),
                                        ((existing_lamp_LCP >= 100) * (existing_lamp_LCP < 150)),
                                        ((existing_lamp_LCP >= 150) * (existing_lamp_LCP < 200)),
                                        ((existing_lamp_LCP >= 200) * (existing_lamp_LCP < 300)),
                                        ((existing_lamp_LCP >= 300) * (existing_lamp_LCP < 500)),
                                        (existing_lamp_LCP >= 500)
                                        ],
                                        [
                                        "existing_lamp_LCP_less_than_100W",
                                        "existing_lamp_LCP_between_100W_and_150W",
                                        "existing_lamp_LCP_between_150W_and_200W",
                                        "existing_lamp_LCP_between_200W_and_300W",
                                        "existing_lamp_LCP_between_300W_and_500W",
                                        "existing_lamp_LCP_more_than_500W"
                                        ]
                                        )

        new_lamp_type = buildings('ESS_HEER_lighting_new_lamp_type', period)
        EquipmentClass = new_lamp_type.possible_values

        is_eligible_new_lamp = (
                (new_lamp_type == EquipmentClass.LED_luminaire_floodlight) +
                (new_lamp_type == EquipmentClass.CFLi)
        )

        new_lamp_type = np.where(is_eligible_new_lamp, 
                new_lamp_type,
                (EquipmentClass.is_not_eligible)
                )



        new_lamp_circuit_power = buildings('ESS_HEER_lighting_new_lamp_circuit_power', period)
        lamp_rating_power = np.select(
                                      [
                                       new_lamp_circuit_power <= 30,
                                       ((new_lamp_circuit_power > 30) * (new_lamp_circuit_power <= 45)),
                                       ((new_lamp_circuit_power > 45) * (new_lamp_circuit_power <= 60)),
                                       ((new_lamp_circuit_power > 60) * (new_lamp_circuit_power <= 90)),
                                       ((new_lamp_circuit_power > 90) * (new_lamp_circuit_power <= 150)),
                                       new_lamp_circuit_power > 150
                                       ],
                                        [
                                        "less_than_or_equal_to_30W",
                                        "more_than_30W_and_less_than_or_equal_to_45W",
                                        "more_than_45W_and_less_than_or_equal_to_60W",
                                        "more_than_60W_and_less_than_or_equal_to_90W",
                                        "more_than_90W_and_less_than_or_equal_to_150W",
                                        "more_than_150W"
                                        ])
        residential_building_savings_factor = (parameters(period).ESS.HEER.table_E2_1.residential_savings_factor
        [LCP_of_existing_lamp]
        [new_lamp_type]
        [lamp_rating_power])
        return residential_building_savings_factor


class ESS_HEER_replace_halogen_floodlight_small_business_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for small business replacements.'

    def formula(buildings, period, parameters):
        existing_lamp_LCP = buildings('ESS_HEER_lighting_existing_lamp_circuit_power', period)
        LCP_of_existing_lamp = np.select(
                                        [
                                        (existing_lamp_LCP < 100),
                                        ((existing_lamp_LCP >= 100) * (existing_lamp_LCP < 150)),
                                        ((existing_lamp_LCP >= 150) * (existing_lamp_LCP < 200)),
                                        ((existing_lamp_LCP >= 200) * (existing_lamp_LCP < 300)),
                                        ((existing_lamp_LCP >= 300) * (existing_lamp_LCP < 500)),
                                        (existing_lamp_LCP >= 500)
                                        ],
                                        [
                                        "existing_lamp_LCP_less_than_100W",
                                        "existing_lamp_LCP_between_100W_and_150W",
                                        "existing_lamp_LCP_between_150W_and_200W",
                                        "existing_lamp_LCP_between_200W_and_300W",
                                        "existing_lamp_LCP_between_300W_and_500W",
                                        "existing_lamp_LCP_more_than_500W"
                                        ]
                                        )

        new_lamp_type = buildings('ESS_HEER_lighting_new_lamp_type', period)
        EquipmentClass = new_lamp_type.possible_values

        is_eligible_new_lamp = (
                (new_lamp_type == EquipmentClass.LED_luminaire_floodlight) +
                (new_lamp_type == EquipmentClass.CFLi)
        )

        new_lamp_type = np.where(is_eligible_new_lamp, 
                new_lamp_type,
                (EquipmentClass.is_not_eligible)
                )

        # above code a. checks if the new lamp type is one of the eligible lamp classes (as defined in the equipment requirements)
        # and b. if it's not eligible, assigns the Enum to a not_eligible product class
        # Table E2.1 now has an appended is_not_eligible index section, with all values set to 0
        # this is kind of hacky but means a. you can use the single list of lighting types and
        # b. you don't have to write out every table with every single class - you can just write what's explicitly written
        # in the rules


        new_lamp_circuit_power = buildings('ESS_HEER_lighting_new_lamp_circuit_power', period)
        lamp_rating_power = np.select(
                                      [
                                       new_lamp_circuit_power <= 30,
                                       ((new_lamp_circuit_power > 30) * (new_lamp_circuit_power <= 45)),
                                       ((new_lamp_circuit_power > 45) * (new_lamp_circuit_power <= 60)),
                                       ((new_lamp_circuit_power > 60) * (new_lamp_circuit_power <= 90)),
                                       ((new_lamp_circuit_power > 90) * (new_lamp_circuit_power <= 150)),
                                       new_lamp_circuit_power > 150
                                       ],
                                        [
                                        "less_than_or_equal_to_30W",
                                        "more_than_30W_and_less_than_or_equal_to_45W",
                                        "more_than_45W_and_less_than_or_equal_to_60W",
                                        "more_than_60W_and_less_than_or_equal_to_90W",
                                        "more_than_90W_and_less_than_or_equal_to_150W",
                                        "more_than_150W"
                                        ])
        small_business_building_savings_factor = (parameters(period).ESS.HEER.table_E2_2.small_business_savings_factor
        [LCP_of_existing_lamp]
        [new_lamp_type]
        [lamp_rating_power])
        return small_business_building_savings_factor
