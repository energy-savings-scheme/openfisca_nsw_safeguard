from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

import numpy as np

class ESS__PFC_real_power_component(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the real power component of the average Site load during' \
            ' operating hours, in kW?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Real Power Component",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }


class ESS__PFC_DistributionDistrict(Enum):
    Endeavour_Energy = 'Implementation takes place in the Endeavour Energy' \
                       ' Distribution District.'
    Essential_Energy = 'Implementation takes place in the Essential Energy' \
                       ' Distribution District.'
    AusGrid = 'Implementation takes place in the Ausgrid Distribution District.'


class ESS__PFC_distribution_district(Variable):
    value_type = Enum
    entity = Building
    possible_values = ESS__PFC_DistributionDistrict
    default_value = ESS__PFC_DistributionDistrict.Endeavour_Energy
    definition_period = ETERNITY
    label = "What Distribution District does the Implementation take place in?"
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Distribution District",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }


class ESS__PFC_initial_power_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the power factor of the load before the installation of' \
            ' the capacitors?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Initial Power Factor",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }


class ESS__PFC_final_power_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the power factor of the load after the installation of' \
            ' the capacitors?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Final Power Factor",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }


class ESS__PFC_installed_capacitors_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the rating of the installed capacitors, in kvar?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Final Power Factor",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }


class ESS__PFC_power_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the Power Savings created by the Power Factor' \
            ' Correction Activity, in kW?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Power Savings",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }

    def formula(buildings, period, parameters):
        real_power = buildings('ESS__PFC_real_power_component', period)
        distribution_district = buildings('ESS__PFC_distribution_district', period)
        distribution_loss_factor = parameters(period).ESS.PFC.table_A19[distribution_district]
        initial_power_factor = buildings('ESS__PFC_initial_power_factor', period)
        initial_power_factor = np.where(initial_power_factor < 0.9,
                                        0.9,
                                        initial_power_factor)
        final_power_factor = buildings('ESS__PFC_final_power_factor', period)
        final_power_factor = np.where(final_power_factor < 0.98,
                                      0.98,
                                      final_power_factor)
        installed_capacitors_rating = buildings('ESS__PFC_installed_capacitors_rating', period)
        power_savings = (real_power * 0.7 * (distribution_loss_factor - 1) * (1 - (initial_power_factor ** 2))
        / (final_power_factor ** 2)) - 0.0039 * (installed_capacitors_rating)
        return power_savings


class ESS__PFC_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the Electricity Savings created by the Power Factor' \
            ' Correction Activity?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Electricity Savings",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }

    def formula(buildings, period, parameters):
        is_eligible = buildings('ESS__PFC_power_factor_correction_meets_eligibility_requirements', period)
        power_savings = buildings('ESS__PFC_power_savings', period)
        operating_hours = parameters(period).ESS.PFC.PFC_related_constants.annual_operating_hours
        site_life = parameters(period).ESS.PFC.PFC_related_constants.site_life
        regional_network_factor = buildings('ESS__regional_network_factor', period)
        electricity_savings = ((power_savings) / 1000 * (operating_hours) * (site_life)
                                * regional_network_factor * is_eligible)
        return electricity_savings
