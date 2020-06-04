# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class B3_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1.'

    def formula(buildings, period, parameters):
        machine_star_rating = buildings('dishwasher_star_rating', period)  # this should be a parameter but it's not in a table in the Rule, pls advise
        number_of_place_settings = buildings('B3_number_of_place_settings', period)
        star_rating = select([
        machine_star_rating == 3.5, machine_star_rating == 4, machine_star_rating == 4.5,
        machine_star_rating == 5, machine_star_rating == 5.5, machine_star_rating == 6,
        machine_star_rating == 7, machine_star_rating == 8, machine_star_rating == 9,
        machine_star_rating == 10],
        ["three_point_five_stars", "four_stars",
        "four_point_five_stars", "five_stars", "five_point_five_stars", "six_stars",
        "seven_stars", "eight_stars", "nine_stars", "ten_stars",
        ])
        place_settings = select([number_of_place_settings < 9,
        number_of_place_settings >= 9 and number_of_place_settings < 13,
        number_of_place_settings >= 13],
        ["less_than_nine_place_settings", "nine_to_thirteen_place_settings",
        "over_thirteen_place_settings"])
        deemed_equipment_electricity_savings = (parameters(period).table_B3_1.deemed_equipment_electricity_savings[star_rating][place_settings])
        return deemed_equipment_electricity_savings
