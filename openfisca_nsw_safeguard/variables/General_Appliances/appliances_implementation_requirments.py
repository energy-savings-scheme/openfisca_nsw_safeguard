from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021


class Appliance_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new product installed?'
    metadata: {
        'alias':  'Is The New Appliance Installed?',
        "regulation_reference": ESS_2021["XX", "GA"]
    }


class Appliance_is_removed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user appliance disconnected and removed?'
    metadata: {
        'alias':  'Is the existing appliance disconnected and removed?',
        "regulation_reference": ESS_2021["XX", "GA"]
    }


class Appliance_follows_removal_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the removal of the appliance follows the removal of appliance requirements under Clause 5.3A? (e.g. Recycled, degassed, not resold etc.)'
    metadata: {
        'alias':  'Is removal of existing appliance follows the requirement under Clause 5.3A?',
        "regulation_reference": ESS_2021["XX", "GA"]
    }


class implementation_is_performed_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference = ""
    label = 'Is the activity performed or supervised by a qualified person in accordance with relevant standards and legislation?'
    # vague guidelines
    metadata: {
        'alias':  'Is the implementation performed by a qualified person?',
        "regulation_reference": ESS_2021["XX", "GA"]
    }
