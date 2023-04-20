from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class RF1_removal_activity_eligibility(Variable):
    """
        Formula to calculate the RF1 removal activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        removal = buildings('RF1_removal', period)
        ACP_engaged = buildings('RF1_engaged_ACP', period)
        primary_refrigeration = buildings('RF1_primary_refrigeration', period)
        residential_building = buildings('RF1_residential_building', period)
        working_order = buildings('RF1_in_working_order', period)
        classified_group = buildings('RF1_classified_group', period)
        capacity_200_litres_or_more = buildings('RF1_capacity_200_litres_or_more', period)

        end_formula = ( removal * ACP_engaged * primary_refrigeration * residential_building *
                        working_order * classified_group *capacity_200_litres_or_more )

        return end_formula