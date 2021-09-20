from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS__SONA_dryer_load(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the load of the dryer, in KG?'


class ESS__SONA_dryer_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the electricity savings for the Implementation?'

    def formula(buildings, period, parameters):
        star_rating = buildings('ESS__SONA_star_rating', period)
        rated_dryer_load = buildings('ESS__SONA_dryer_load', period)

        dryer_load = np.select([(rated_dryer_load < 5),
        ((rated_dryer_load >= 5) * (rated_dryer_load < 8)),
        (rated_dryer_load >= 8)],
        ["less_than_5kg",
        "between_5kg_and_8kg",
        "more_than_8kg"])

        deemed_equipment_electricity_savings = (parameters(period).
        ESS.SONA.table_B2_1.deemed_equipment_electricity_savings[star_rating][dryer_load])

        return deemed_equipment_electricity_savings
