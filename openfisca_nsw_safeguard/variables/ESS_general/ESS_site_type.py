from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS_SiteType(Enum):
    residential = 'Activity takes place in a Residential Site.'
    small_business = 'Activity takes place in a Small Business Site.'
    other = 'Activity takes place in another type of site.'
    # list is likely incomplete


class ESS_site_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = ESS_SiteType
    default_value = ESS_SiteType.residential
    definition_period = ETERNITY
    label = 'What BCA climate zone is the activity taking place in?'
    metadata={
        "variable-type": "user-input",
        "alias":"ESS Site Type",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Energy Savings Scheme - General'
        }
