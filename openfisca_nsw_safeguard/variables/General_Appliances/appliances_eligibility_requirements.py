from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import ESS_2021


class Appliance_located_in_residential_building(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Site is located in a residential building?'
    metadata: {
        'alias':  'Site is located in a residential building?',
        "regulation_reference": ESS_2021.json()

    }


class Appliance_located_in_small_biz_building(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Site is located in a small business building?'
    metadata: {
        'alias':  'Site is located in a small business building?',
        "regulation_reference": ESS_2021.json()
    }
