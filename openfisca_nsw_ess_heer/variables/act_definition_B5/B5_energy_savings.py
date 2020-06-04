# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class B5_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1.'

    def formula(buildings, period, parameters):
        machine_star_rating = buildings('refrigerator_star_rating', period)  # this should be a parameter but it's not in a table in the Rule, pls advise
        refrigerator_volume = buildings('refrigerator_or_freezer_capacity', period)
        star_rating = select([
        machine_star_rating == 3.5, machine_star_rating == 4,
        machine_star_rating == 4.5, machine_star_rating == 5, machine_star_rating == 5.5,
        machine_star_rating == 6, machine_star_rating == 7, machine_star_rating == 8,
        machine_star_rating == 9, machine_star_rating == 10],
        ["three_point_five_stars", "four_stars",
        "four_point_five_stars", "five_stars", "five_point_five_stars", "six_stars",
        "seven_stars", "eight_stars", "nine_stars", "ten_stars",
        ])
        volume = select([refrigerator_volume < 300,
        refrigerator_volume >= 300 and refrigerator_volume < 450,
        refrigerator_volume >= 450 and refrigerator_volume < 550,
        refrigerator_volume >= 550],
        ["volume_less_than_300_litres", "volume_300_to_450_litres",
        "volume_450_to_550_litres", "volume_550_litres_or_over"])
        deemed_equipment_electricity_savings = (parameters(period).table_B5_1.deemed_equipment_electricity_savings[star_rating][volume])
        return deemed_equipment_electricity_savings
