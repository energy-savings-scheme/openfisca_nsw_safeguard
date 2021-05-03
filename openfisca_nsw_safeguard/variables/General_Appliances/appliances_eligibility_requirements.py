from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class Appliance_located_in_residential_building(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Site is located in a residential building?'
    metadata: {
        'alias':  'Site is located in a residential building?'
    }


class Appliance_located_in_small_biz_building(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Site is located in a small business building?'
    metadata: {
        'alias':  'Site is located in a small business building?'
    }
