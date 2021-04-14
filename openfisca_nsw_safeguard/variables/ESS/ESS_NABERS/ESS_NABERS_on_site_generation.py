from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY, YEAR
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class all_on_site_sources_identified(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = "Have all the sources of on-site electricity generation been identified?"


class unaccounted_elec_metered_and_recorded(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = 'Has all electricity generated from sources of On-site Unaccounted' \
            ' Electricity (as referred to in Method 4) been metered and' \
            ' recorded over the Rating Period?'
