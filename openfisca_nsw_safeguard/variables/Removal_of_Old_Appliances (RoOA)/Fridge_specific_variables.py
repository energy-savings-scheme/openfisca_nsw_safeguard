from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class Fridge_is_classified_as_refrigerator(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing equipment classified as a refrigerator under the following Group 1, 2, 3, 4, 5T, 5B, 5S, 6C, 6U, 7?'
    metadata: {
        'alias':  'The existing equipment is classified as a refrigerator',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }


class Fridge_not_primary(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is there another fridge/freezer at the site that provides primary refrigeration or freezing services? '
    metadata: {
        'alias':  'Fridge is not primary',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }


class Fridge_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the fridge/freezer being removed in working order? '
    metadata: {
        'alias':  'Fridge is in working order',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }


class Fridge_capacity_more_than_200L(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the capacity of the fridge 200 liters or more? '
    metadata: {
        'alias':  'Fridge capacity is more than 200L',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }


class Fridge_total_number_one_less(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'As a result of the activity, there must be ONE fewer fridge/freezer at the site.'
    metadata: {
        'alias':  'One less fridge/freezer on the site',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }
