from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY, YEAR
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

import numpy as np
from datetime import date


class ESS__PIAMV_NRE_is_submetered(Variable):
    value_type = bool
    default_value = False
    entity = Building
    definition_period = ETERNITY
    label = 'Is the NRE as part of the PIAMV method submetered?'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"ESS PIAMV NRE Is Submetered",
        }


class ESS__PIAMV_NRE_caused_by_other_implementations(Variable):
    value_type = bool
    default_value = False
    entity = Building
    definition_period = ETERNITY
    label = 'Is the NRE as part of the PIAMV method caused by other implementations?'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"ESS PIAMV NRE Is Caused By Other Implementations",
        }

class ESS__PIAMV_NRE_is_permanent(Variable):
    value_type = bool
    default_value = False
    entity = Building
    definition_period = ETERNITY
    label = 'Is the NRE permanent?'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"ESS PIAMV NRE Is Caused By Other Implementations",
        }


class ESS__PIAMV_NRE_happens_in_first_25_percent_of_measurement_period(Variable):
    value_type = bool
    default_value = False
    entity = Building
    definition_period = ETERNITY
    label = 'Is the NRE permanent?'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"ESS PIAMV NRE Is Caused By Other Implementations",
        }


class ESS__PIAMV_measurement_period_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the length of the measurement period, in days?'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"ESS PIAMV NRE Is Caused By Other Implementations",
        }


class ESS__PIAMV_NRE_period_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'What is the length of the NRE, in days?'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"ESS PIAMV NRE Is Caused By Other Implementations",
        }


class ESS__PIAMV_NRE_is_less_than_25_percent(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the NRE less than 25 percent of the PIAMV Measurement Period Length?'
    metadata={
        "variable-type": "inter-interesting", # need to check this metadata
        "alias":"ESS PIAMV NRE Less than 25 Percent of Measurement Period",
        }

    def formula(buildings, period, parameters):
        measurement_period_length = buildings('ESS__PIAMV_measurement_period_length', period)
        # measured in days?
        NRE_period_length = buildings('ESS__PIAMV_NRE_period_length', period)
        # measured in days?
        return (
                (NRE_period_length / measurement_period_length) 
                <= 0.25
                )