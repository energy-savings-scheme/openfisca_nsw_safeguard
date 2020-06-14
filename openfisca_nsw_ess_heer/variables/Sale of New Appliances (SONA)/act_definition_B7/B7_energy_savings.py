# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class B7_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1.'

    def formula(buildings, period, parameters):
        television_star_rating = buildings('television_star_rating', period)  # this should be a parameter but it's not in a table in the Rule, pls advise
        television_screen_size = buildings('television_screen_size', period)
        star_rating = select([television_star_rating < 7,
        television_star_rating == 7, television_star_rating == 8,
        television_star_rating == 9, television_star_rating == 10],
        ["under_seven_stars", "seven_stars", "eight_stars", "nine_stars", "ten_stars"])
        screen_size = select([television_screen_size < 40,
        television_screen_size > 40 and television_screen_size <= 65,
        television_screen_size > 65 and television_screen_size <= 120,
        television_screen_size >= 120],
        ["under_40cm", "40_to_65cm", "65_to_120cm", "over_120cm"])
        deemed_equipment_electricity_savings = (parameters(period).table_B7_1.deemed_equipment_electricity_savings[star_rating][screen_size])
        return deemed_equipment_electricity_savings
