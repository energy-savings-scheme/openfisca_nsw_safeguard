from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021

class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_existing_pool_pump_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is there an existing pool pump at the Site?'
    metadata = {
        'alias':  'Existing pool pump is at the Site.',
        "regulation_reference": PDRS_2022["XX", "pool pump"]
    }


class PDRS_replace_existing_pool_pump_with_high_efficiency_pump_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the Eligibility Requirements?'
    metadata = {
        'alias':  'PDRS Pool Pump Activity Meets Eligibility Requirements',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }

    def formula(buildings, period, parameters):
        existing_pool_pump_is_installed = buildings(
            'PDRS_replace_existing_pool_pump_with_high_efficiency_pump_existing_pool_pump_is_installed', period)
        return existing_pool_pump_is_installed