# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class C1_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the energy savings for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1.'

    def formula(buildings, period, parameters):
        elec_savings = 5.7  # this should be a parameter but it's not in a table in the Rule, pls advise
        C1_requirements_are_met = buildings('C1_requirements_are_met', period)
        condition_requirements_are_met = (C1_requirements_are_met)
        return where(condition_requirements_are_met, elec_savings, 0)
