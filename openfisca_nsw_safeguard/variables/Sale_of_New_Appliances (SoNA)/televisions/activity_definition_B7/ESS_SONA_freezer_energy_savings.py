from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_SONA_television_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B7.'

    def formula(buildings, period, parameters):
        star_rating = buildings('television_star_rating', period)  # this should be a parameter but it's not in a table in the Rule, pls advise
        television_screen_size = buildings('television_screen_size', period)
        screen_size = select([television_screen_size < 40,
        television_screen_size > 40 and television_screen_size <= 65,
        television_screen_size > 65 and television_screen_size <= 120,
        television_screen_size >= 120],
        ["under_40cm", "40_to_65cm", "65_to_120cm", "over_120cm"])
        deemed_equipment_electricity_savings = (parameters(period).SONA.table_B7_1.deemed_equipment_electricity_savings[star_rating][screen_size])
        return deemed_equipment_electricity_savings
