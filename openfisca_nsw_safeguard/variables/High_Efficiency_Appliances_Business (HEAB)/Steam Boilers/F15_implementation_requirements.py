# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F15_installed_in_accordance_with_manufacturer_guidelines(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with manufacturer guidelines?'


class F15_installed_in_accordance_with_relevant_standards_and_legislation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with relevant standards' \
            ' and legislation?'


class F15_installed_in_accordance_with_scheme_administrator_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with other Scheme' \
            ' Administrator Requirements?'


class F15_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F15?'

    def formula(buildings, period, parameters):
        adheres_to_manufacturers_guidelines = buildings('F15_installed_in_accordance_with_manufacturer_guidelines', period)
        adheres_to_relevants_standards_and_legislation = buildings('F15_installed_in_accordance_with_relevant_standards_and_legislation', period)
        adheres_to_scheme_administrator_requirements = buildings('F15_installed_in_accordance_with_scheme_administrator_requirements', period)
        return(adheres_to_manufacturers_guidelines * adheres_to_relevants_standards_and_legislation
              * adheres_to_scheme_administrator_requirements)
