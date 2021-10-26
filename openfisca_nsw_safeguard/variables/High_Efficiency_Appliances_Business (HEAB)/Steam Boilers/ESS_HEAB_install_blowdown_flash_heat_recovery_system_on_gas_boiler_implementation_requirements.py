from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np



class ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_installed_in_accordance_with_manufacturer_guidelines(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with manufacturer guidelines?'


class ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_installed_in_accordance_with_relevant_standards_and_legislation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with relevant standards' \
            ' and legislation?'


class ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_installed_in_accordance_with_scheme_administrator_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with other Scheme' \
            ' Administrator Requirements?'


class ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F14?'

    def formula(buildings, period, parameters):
        adheres_to_manufacturers_guidelines = buildings('F14_installed_in_accordance_with_manufacturer_guidelines', period)
        adheres_to_relevants_standards_and_legislation = buildings('F14_installed_in_accordance_with_relevant_standards_and_legislation', period)
        adheres_to_scheme_administrator_requirements = buildings('F14_installed_in_accordance_with_scheme_administrator_requirements', period)
        return(adheres_to_manufacturers_guidelines * adheres_to_relevants_standards_and_legislation
              * adheres_to_scheme_administrator_requirements)
