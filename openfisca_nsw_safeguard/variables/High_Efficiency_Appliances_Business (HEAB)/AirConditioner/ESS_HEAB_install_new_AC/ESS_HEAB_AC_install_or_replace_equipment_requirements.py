import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS_HEAB_install_or_replace_AC_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the equipment meet all of the Equipment' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC Install meets equipment requirements",
    }

    def formula(buildings, period, parameters):
        is_in_GEMS = buildings(
            'Appliance_is_registered_in_GEMS', period)

        TCSPF_or_AEER_exceeds_benchmark = buildings('AC_TCSPF_or_AEER_exceeds_ESS_benchmark', period)
        HSPF_or_ACOP_exceeds_benchmark = buildings('AC_HSPF_or_ACOP_exceeds_ESS_benchmark', period)

        return(
            is_in_GEMS *
            TCSPF_or_AEER_exceeds_benchmark * 
            HSPF_or_ACOP_exceeds_benchmark
        )        