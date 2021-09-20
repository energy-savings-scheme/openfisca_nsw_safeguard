from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_SONA_1_door_refrigerator_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B4.'

    def formula(buildings, period, parameters):
        star_rating = buildings('refrigerator_star_rating', period)  # this should be a parameter but it's not in a table in the Rule, pls advise
        refrigerator_volume = buildings('refrigerator_or_freezer_capacity', period)
        volume = np.select([refrigerator_volume < 200,
        ((refrigerator_volume >= 200) * (refrigerator_volume < 250)),
        refrigerator_volume >= 250],
        ["volume_less_than_200_litres", "volume_200_to_250_litres",
        "volume_over_250_litres"])
        deemed_equipment_electricity_savings = (parameters(period).ESS.SONA.table_B4_1.deemed_equipment_electricity_savings[star_rating][volume])
        return deemed_equipment_electricity_savings


class ESS_SONA_1_door_refrigerator_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings for the Implementation, if eligible?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B4.'

    def formula(buildings, period, parameters):
        elec_savings = buildings('ESS_SONA_1_door_refrigerator_electricity_savings', period)
        is_eligible = buildings('ESS_SONA_1_door_refrigerator_meets_all_equipment_requirements', period)
        return elec_savings * is_eligible
