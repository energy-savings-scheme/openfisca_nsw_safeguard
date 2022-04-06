from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021

class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_existing_pump_decommissioned_according_to_relevant_legislation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the decommissioned pool pump removed in accordance with relevant standards and legislation?'
    metadata = {
        'alias':  'Decommissioned pool pump removed in accordance with legislation',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }


class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the Implementation Requirements?'
    metadata = {
        'alias':  'PDRS Pool Pump Activity Meets Eligibility Requirements',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        performed_by_qualified_person = buildings(
            'implementation_is_performed_by_qualified_person', period)
        removed_according_to_legislation = buildings(
            'PDRS_replace_existing_pool_pump_with_high_efficiency_pump_existing_pump_decommissioned_according_to_relevant_legislation', period)
        return(
            performed_by_qualified_person *
            removed_according_to_legislation
        )