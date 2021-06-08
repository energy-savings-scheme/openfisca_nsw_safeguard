from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from datetime import date
import numpy as np

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

class ESS__PFC_electricity_from_network_less_than_50kV(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the electricity supplied from the Electricity Network less than' \
            ' 50kV at the site where the power factor correction services are' \
            ' being conducted?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PFC Electricity from Network Less Than 50kV",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }

    def formula(buildings, period, parameters):
        network_voltage = buildings('ESS__PFC_network_voltage', period)
        return network_voltage < 50
        # note we should probably put the maximum kV in a table or something, \
        # and link to a parameter file here


class ESS__PFC_network_voltage(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the voltage of the electricity supplied from the' \
            ' Electricity Network to the site where the power factor correction' \
            ' services are being conducted, in kV?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Network Voltage",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }


class ESS__PFC_lagging_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the lagging achieved by the capacitors installed at the Site?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Lagging Factor",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }


class ESS__PFC_minimum_lagging_factor(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Do the capacitors achieve the required minimum of 0.9 lagging?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Minimum Lagging Factor",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }

    def formula(buildings, period, parameters):
        lagging_factor = buildings('ESS__PFC_lagging_factor', period)
        return lagging_factor > 0.9


class ESS__PFC_capacitors_are_installed_as_part_of_mandatory_program(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Are the capacitors installed as part of a mandatory program of installation?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Capacitors Installed as Part of Mandatory Program",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }
    # reminder that capacitors cannot be installed as part of a mandatory installation program


class ESS__PFC_capacitors_installed_at_main_switchboard(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Are the capacitors installed at the main switchboard?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Capacitors Installed at Main Switchboard",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }


class ESS__PFC_site_is_connected_to_electricity_network(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the site connected to an Electricity Network?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Capacitors Installed as Part of Mandatory Program",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }
    # need to check if the site needs to be connected to any form of \
    # Network to conduct this activity.


class ESS__PFC_installed_capacitors_are_new(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Are the installed capacitors new?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Capacitors Installed Are New",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }


class ESS__PFC_date_of_capacitor_installation(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the date at which the capacitors were installed?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Capacitors Installation Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }


class ESS__PFC_implementation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Implementation Date for the Power Factor Correction' \
            ' energy savings activity?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PFC Implementation Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }

    def formula(buildings, period, parameters):
        capacitor_installation_date = buildings('date_of_capacitor_installation', period)
        return capacitor_installation_date


class ESS__PFC_purchaser(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Who is the Purchaser for the Power Factor Correction' \
            ' energy savings activity?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Purchaser",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }


class ESS__PFC_energy_saver(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Who is the Energy Saver for the Power Factor Correction' \
            ' energy savings activity?'
    metadata = {
        "variable-type": "user-input",
        "alias": "PFC Energy Saver",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Deemed Energy Savings Method - Power Factor Crrection'
        "regulation_reference": ESS_2021["9", "9.6"]
    }
    # note that for PFCESF, the Purchaser is the Energy Saver.

    def formula(buildings, period, parameters):
        purchaser = buildings('ESS__PFC_purchaser', period)
        return purchaser


class ESS__PFC_power_factor_correction_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Implementation meet all of the eligibility requirements' \
            ' for Power Factor Correction energy savings activities?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.6 - Power Factor Correction Energy Savings Formula.'

    def formula(buildings, period, parameters):
        electricity_supplied_from_network_less_than_50kV = buildings(
            'ESS__PFC_electricity_from_network_less_than_50kV', period)
        achieves_minimum_lagging_factor = buildings(
            'ESS__PFC_minimum_lagging_factor', period)
        installed_as_part_of_mandatory_program = buildings(
            'ESS__PFC_capacitors_are_installed_as_part_of_mandatory_program', period)
        site_connected_to_network = buildings(
            'ESS__PFC_site_is_connected_to_electricity_network', period)
        capacitors_installed_at_main_switchboard = buildings(
            'ESS__PFC_capacitors_installed_at_main_switchboard', period)
        installed_capacitors_are_new = buildings('ESS__PFC_installed_capacitors_are_new', period)
        return (electricity_supplied_from_network_less_than_50kV
                * achieves_minimum_lagging_factor
                * (np.logical_not(installed_as_part_of_mandatory_program))
                * site_connected_to_network
                * capacitors_installed_at_main_switchboard
                * installed_capacitors_are_new)
