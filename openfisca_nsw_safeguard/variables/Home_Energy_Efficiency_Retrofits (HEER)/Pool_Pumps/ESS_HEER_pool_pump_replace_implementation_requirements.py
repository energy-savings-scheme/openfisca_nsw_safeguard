from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import ESS_2021

class ESS_HEER_pool_pump_replace_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet the Implementation Requirements detailed in Activity Definition D5?'
    metadata = {
        'alias':  'ESS HEER Pool Pump Replace Meets Implementation Requirements',
    }

    def formula(buildings, period, parameters):
        existing_equipment_removed = buildings('Equipment_is_removed', period)
        performed_by_qualified_person = buildings(
            'implementation_is_performed_by_qualified_person', period)
        return(
            existing_equipment_removed *
            performed_by_qualified_person
        )


class ESS_HEER__replace_existing_pool_pump_new_product_is_for_domestic_use(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product for domestic use in a pool or spa?'
    metadata = {
        'alias':  'New product for domestic use.',
    }
