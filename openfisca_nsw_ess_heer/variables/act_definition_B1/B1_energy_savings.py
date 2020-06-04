# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class B1_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1.'

    def formula(buildings, period, parameters):
        machine_star_rating = buildings('washing_machine_star_rating', period)  # this should be a parameter but it's not in a table in the Rule, pls advise
        machine_washing_load = buildings('B1_end_user_equipment_load', period)
        star_rating = select([machine_star_rating == 4, machine_star_rating == 4.5,
        machine_star_rating == 5, machine_star_rating == 5.5, machine_star_rating >= 6],
        ["four_stars", "four_point_five_stars", "five_stars", "five_point_five_stars",
        "six_stars_or_above"])
        washing_load = select([machine_washing_load <= 4,
        machine_washing_load > 4 and machine_washing_load <= 6.5,
        machine_washing_load > 6.5 and machine_washing_load <= 7,
        machine_washing_load > 7 and machine_washing_load <= 7.5,
        machine_washing_load > 7.5],
        ["less_than_4kg", "between_4kg_and_6_and_a_half_kg",
        "between_6_and_a_half_and_7kg", "between_7kg_and_7_and_a_half_kg",
        "more_than_7_and_a_half_kg"])
        deemed_equipment_electricity_savings = (parameters(period).table_B1_1.deemed_equipment_electricity_savings[star_rating][washing_load])
        return deemed_equipment_electricity_savings


class C1_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1.'

    def formula(buildings, period, parameters):
        elec_savings = buildings('B1_electricity_savings', period) # this should be a parameter but it's not in a table in the Rule, pls advise
        B1_requirements_are_met = buildings('B1_meets_all_equipment_requirements', period)
        condition_requirements_are_met = (B1_requirements_are_met == True)
        return where(condition_requirements_are_met, elec_savings, 0)
