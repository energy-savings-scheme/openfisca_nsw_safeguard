from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

class PDRS_RF2_replace_refrigerated_cabinet_activity_is_replacement_of_RC(BaseVariable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity the installation or replacement of a Refrigerated Cabinet?'
    metadata = {
        'alias':  'The existing equipment is classified as a refrigerator',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }


class PDRS_RF2_replace_refrigerated_cabinet_meets_eligibility_requirements(BaseVariable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the Eligibility Requirements?'
    metadata = {
        'alias':  'The existing equipment is classified as a refrigerator',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        activity_is_replacing_RC = buildings(
            'PDRS_RF2_replace_refrigerated_cabinet_activity_is_replacement_of_RC', period)
        return activity_is_replacing_RC