from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY, YEAR
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

import numpy as np
from datetime import date


class ESS__PIAMV_exercise_date_variable(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'Sample Float Variable'
    metadata={
        "alias":"Sample Date Variable",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - PIAM&V      
        }


class ESS__PIAMV_energy_saver_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What date has the ACP become the energy saver?'
    metadata={
        "alias":"Energy Saver Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - PIAM&V      
        }


class ESS__PIAMV_ACP_accreditation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What date has the ACP become accredited?'
    metadata={
        "alias":"ACP Accreditation Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - PIAM&V      
        }


class ESS__PIAMV_ACP_implementation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What date has the ACP become accredited?'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"ACP Accreditation Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - PIAM&V      
        }


class ESS__PIAMV_is_eligible_to_create_ESCs(Variable):
    value_type = bool
    default_value = False
    entity = Building
    definition_period = ETERNITY
    label = 'Is the ACP eligible to create ESCs?'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"ACP Accreditation Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - PIAM&V      
        }

    def formula(buildings, period, parameters):
        energy_saver_date = buildings('ESS__PIAMV_energy_saver_date', period)
        accreditation_date = buildings('ESS__PIAMV_ACP_accreditation_date', period)
        implementation_date = buildings('ESS__PIAMV_ACP_implementation_date', period)
        accreditation_before_implementation_date = (
            accreditation_date < implementation_date
        )
        is_energy_saver_before_implementation = (
            energy_saver_date < implementation_date
        )
        is_eligible = (
            accreditation_before_implementation_date *
            is_energy_saver_before_implementation
        )
        return is_eligible
    