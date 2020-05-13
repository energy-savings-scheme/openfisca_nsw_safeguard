# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class new_equipment_applied_to_existing_fan(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new equipment is applied to the existing' \
            ' exhaust fan, as required by Implementation Requirement 1.'


class new_equipment_restricts_airflow(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new equipment effectively restricts airflow' \
            ' into or out of the site, as required by Implementation Requirement 2.'


class E12_product_installed_according_to_instructions(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product has been installed in strict accordance' \
            ' with the manufacturer instructions, as prescribed by' \
            ' Implementation Requirement 3.'


class E12_electricial_work_performed_by_electrician(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether all electrical work has been performed by a' \
            ' licensed electrician, as prescribed by Implementation' \
            ' Requirement 4.'


class all_exhaust_fans_are_sealed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether all exhaust fan at the site have been sealed,' \
            ' as prescribed by Implementation Requirement 5.'


class complies_with_relevant_standards(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the installed new equipment complies with relevant,' \
            ' AS or NZS standards, as prescribed by Implementation Requirement 5.'
