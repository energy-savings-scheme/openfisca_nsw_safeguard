from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class C1_PDRSAug24_removal_activity_eligibility(Variable):
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
        removal = buildings('C1_PDRSAug24_removal', period)
        ACP_engaged = buildings('C1_PDRSAug24_engaged_ACP', period)
        primary_refrigeration = buildings('C1_PDRSAug24_primary_refrigeration', period)
        residential_building = buildings('C1_PDRSAug24_residential_building', period)
        working_order = buildings('C1_PDRSAug24_in_working_order', period)
        classified_group = buildings('C1_PDRSAug24_classified_group', period)
        capacity_200_litres_or_more = buildings('C1_PDRSAug24_capacity_200_litres_or_more', period)

        end_formula = ( removal * ACP_engaged * primary_refrigeration * residential_building *
                        working_order * classified_group * capacity_200_litres_or_more )

        return end_formula