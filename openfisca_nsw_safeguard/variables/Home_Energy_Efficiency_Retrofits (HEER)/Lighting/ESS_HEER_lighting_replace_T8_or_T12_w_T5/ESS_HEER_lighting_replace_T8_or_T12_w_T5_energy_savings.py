from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_HEER_lighting_replace_T8_or_T12_w_T5_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

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
                        buildings('ESS_HEER_lighting_replace_T8_or_T12_w_T5_residential_savings_factor', period),
                        buildings('ESS_HEER_lighting_replace_T8_or_T12_w_T5_small_business_savings_factor', period),
                        0
                ]
                )

        return electricity_savings



class ESS_HEER_lighting_replace_T8_or_T12_w_T5_residential_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        lamp_size = buildings('ESS_HEER_existing_lamp_length', period)
        size_of_existing_lamp = np.select(
                                          [
                                          lamp_size == 2,
                                          lamp_size == 3,
                                          lamp_size == 4,
                                          lamp_size == 5
                                           ],
                                          [
                                           "2_foot",
                                           "3_foot",
                                           "4_foot",
                                           "5_foot"
                                           ]
                                           )
        residential_building_savings_factor = (parameters(period).
        ESS.HEER.table_E4_1.residential_savings_factor[size_of_existing_lamp])
        return residential_building_savings_factor


class ESS_HEER_lighting_replace_T8_or_T12_w_T5_small_business_savings_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the relevant savings factor for the existing and new lamp' \
            ' for residential replacements.'

    def formula(buildings, period, parameters):
        lamp_size = buildings('ESS_HEER_existing_lamp_length', period)
        size_of_existing_lamp = np.select(
                                          [
                                          lamp_size == 2,
                                          lamp_size == 3,
                                          lamp_size == 4,
                                          lamp_size == 5
                                           ],
                                          [
                                           "2_foot",
                                           "3_foot",
                                           "4_foot",
                                           "5_foot"
                                           ]
                                           )
        small_business_savings_factor = (parameters(period).
        ESS.HEER.table_E4_2.small_business_savings_factor[size_of_existing_lamp])
        return small_business_savings_factor
