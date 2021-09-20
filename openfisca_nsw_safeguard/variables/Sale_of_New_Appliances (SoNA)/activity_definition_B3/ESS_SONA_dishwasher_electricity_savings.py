from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS__SONA_dishwasher_number_of_place_settings(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'How many place settings does the dishwasher have?'


class ESS__SONA_dishwasher_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the electricity savings for the Implementation?'

    def formula(buildings, period, parameters):
        star_rating = buildings('ESS__SONA_star_rating', period)
        number_of_place_settings = buildings('ESS__SONA_dishwasher_number_of_place_settings', period)

        place_settings = np.select([(number_of_place_settings < 9),
        ((number_of_place_settings >= 9) * (number_of_place_settings < 13)),
        (number_of_place_settings >= 13)],
        ["less_than_9_place_settings",
        "between_9_and_13_place_settings",
        "13_or_more_place_settings"])

        deemed_equipment_electricity_savings = (parameters(period).
        ESS.SONA.table_B3_1.deemed_equipment_electricity_savings[star_rating][place_settings])

        return deemed_equipment_electricity_savings
