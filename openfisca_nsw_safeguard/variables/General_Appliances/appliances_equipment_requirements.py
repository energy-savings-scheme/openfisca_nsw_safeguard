from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import ESS_2021, PDRS_2022


class Appliance_is_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new product registered in GEMS?'
    metadata = {
        'alias':  'Appliance is registered in GEMS',
        "regulation_reference": ESS_2021["XX", "GA"]
    }


class Appliance_demand_response_capability(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the end user equipment have demand response capability in modes DRM1, DRM2 and DRM3 in accordance with AS4755.3.1?'
    metadata = {
        'alias':  'Appliance has demand response capability',
        "regulation_reference": PDRS_2022["XX", "GA"]
    }
