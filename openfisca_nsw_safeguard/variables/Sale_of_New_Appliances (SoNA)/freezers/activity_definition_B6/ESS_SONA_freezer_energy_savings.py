from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_SONA_freezer_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the deemed electricity savings for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1.'

    def formula(buildings, period, parameters):
        star_rating = buildings('refrigerator_star_rating', period)  # this should be a parameter but it's not in a table in the Rule, pls advise
        freezer_volume = buildings('refrigerator_or_freezer_capacity', period)
        volume = select([freezer_volume < 150, freezer_volume >= 150 and freezer_volume < 300,
        freezer_volume >= 300 and freezer_volume < 500, freezer_volume >= 550],
        ["under_150L", "150_to_300L", "300_to_500L", "over_500L"])
        deemed_equipment_electricity_savings = (parameters(period).SONA.table_B6_1.deemed_equipment_electricity_savings[star_rating][volume])
        return deemed_equipment_electricity_savings


class ESS_SONA_freezer_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings for the Implementation, if eligible?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1.'

    def formula(buildings, period, parameters):
        elec_savings = buildings('ESS_SONA_freezer_electricity_savings', period)
        is_eligible = buildings('ESS_SONA_freezer_meets_all_equipment_requirements', period)
        return elec_savings * is_eligible
