from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY, YEAR
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021


class all_on_site_sources_identified(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = "Have all the sources of on-site electricity generation been identified?"
    metadata = {
        "variable-type": "user-input",
        "alias": "NABERS All On Site Electricity Generation Sources Identified",
        "regulation_reference": ESS_2021["8", "8.8"]
    }


class unaccounted_elec_metered_and_recorded(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has all electricity generated from sources of On-site Unaccounted' \
            ' Electricity (as referred to in Method 4) been metered and' \
            ' recorded over the Rating Period?'
    metadata = {
        "variable-type": "user-input",
        "alias": "NABERS Unaccounted Electricity Metered and Recorded",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8", "8.8"]
    }
