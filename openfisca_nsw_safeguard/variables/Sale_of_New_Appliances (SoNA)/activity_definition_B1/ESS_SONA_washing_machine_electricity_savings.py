from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS__SONA_washing_machine_load(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the load of the washing machine, in KG?'


class ESS__SONA_washing_machine_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the electricity savings for the Implementation?'

    def formula(buildings, period, parameters):
        star_rating = buildings('ESS__SONA_star_rating', period)
        washing_machine_load = buildings('ESS__SONA_washing_machine_load', period)

        washing_load = np.select([(washing_machine_load <= 4),
        ((washing_machine_load > 4) * (washing_machine_load <= 6.5)),
        ((washing_machine_load > 6.5) * (washing_machine_load <= 7)),
        ((washing_machine_load > 7) * (washing_machine_load <= 7.5)),
        (washing_machine_load > 7.5)],
        ["less_than_4kg", "between_4kg_and_6_and_a_half_kg",
        "between_6_and_a_half_and_7kg", "between_7kg_and_7_and_a_half_kg",
        "more_than_7_and_a_half_kg"])

        deemed_equipment_electricity_savings = (parameters(period).ESS.SONA.table_B1_1.deemed_equipment_electricity_savings[star_rating][washing_load])

        return deemed_equipment_electricity_savings
