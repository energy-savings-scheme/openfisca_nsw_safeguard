import numpy as np

from openfisca_core.periods import ETERNITY

from openfisca_nsw_safeguard.entities import Building
from openfisca_nsw_safeguard.base_variables import BaseVariable


class ESS_HEAB_install_or_replace_AC_meets_implementation_requirements(BaseVariable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Implementation' \
            ' Requirements defined in installing a high efficiency air conditioner for Business?'
    metadata = {
        'alias': "HEAB AC Install meets implementation requirements",
    }

    def formula(buildings, period, parameters):
        is_installed = buildings(
            'Equipment_is_installed', period)
        performed_by_qualified_person = buildings(
            'Implementation_is_performed_by_qualified_person', period)

        return (
                is_installed * 
                performed_by_qualified_person
                )