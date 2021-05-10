from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class No_Existing_AC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is there existing air conditioner fixed in place that provides cooling to the conditioned space?'
    metadata: {
        'alias':  'No Existing Air Conditioner fixed in place',
        "regulation_reference": PDRS_2022["XX", "AC"]
    }


class AC_has_5_years_warranty(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Air Conditioner has at least 5 years of Warranty?'
    metadata: {
        'alias':  'Air Conditioner has at least 5 years of Warranty',
        "regulation_reference": PDRS_2022["XX", "AC"]
    }
