from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class RCProductClass(Enum):
    product_class_one = 'RDC is in product class 1.'
    product_class_two = 'RDC is in product class 2.'
    product_class_three = 'RDC is in product class 3.'
    product_class_four = 'RDC is in product class 4.'
    product_class_five = 'RDC is in product class 5.'
    product_class_six = 'RDC is in product class 6.'
    product_class_seven = 'RDC is in product class 7.'
    product_class_eight = 'RDC is in product class 8.'
    product_class_nine = 'RDC is in product class 9.'
    product_class_ten = 'RDC is in product class 10.'
    product_class_eleven = 'RDC is in product class 11.'
    product_class_twelve = 'RDC is in product class 12.'
    product_class_thirteen = 'RDC is in product class 13.'
    product_class_fourteen = 'RDC is in product class 14.'
    product_class_fifteen = 'RDC is in product class 15.'


class refrigerated_cabinet_product_class(Variable):
    value_type = Enum
    entity = Building
    possible_values = RCProductClass
    default_value = RCProductClass.product_class_one
    definition_period = ETERNITY
    label = 'What is the product class for the refrigerated cabinet?'


class RCDutyClass(Enum):
    heavy_duty = 'RDC is a heavy duty RC.'
    normal_duty = 'RDC is a normal duty RC.'
    light_duty = 'RDC is a light duty RC.'


class refrigerated_cabinet_duty_class(Variable):
    value_type = Enum
    entity = Building
    possible_values = RCDutyClass
    default_value = RCDutyClass.normal_duty
    definition_period = ETERNITY
    label = 'What is the duty class for the refrigerated cabinet?'


class new_refrigerated_cabinet_EEI(Variable):
    value_type = float
    entity = Building
    default_value = 0
    definition_period = ETERNITY
    label = 'What is the EEI of the new refrigerated cabinet?'


class new_refrigerated_cabinet_total_energy_consumption(Variable):
    value_type = float
    entity = Building
    default_value = 0
    definition_period = ETERNITY
    label = 'What is the total energy consumption of the new refrigerated cabinet?'


class new_refrigerated_cabinet_total_display_area(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the total display area of the Refrigerated Cabinet, in m2?'
    metadata = {
        'alias':  'RC Input Power',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }


class ESS_HEAB_refrigerated_cabinet_is_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new refrigerated cabinet registered in the GEMS Registry?'
    metadata = {
        'alias':  'The existing equipment is classified as a refrigerator',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }


class ESS_HEAB_new_equipment_is_RC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a Refrigerated Cabinet?'
    metadata = {
        'alias':  'The existing equipment is classified as a refrigerator',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }


class ESS_HEAB_number_of_RCs_installed(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'How many ?'
    metadata = {
        'alias':  'How many RCs are being installed or replaced as part of the implementation?',
        "regulation_reference": PDRS_2022["XX", "fridge"]
    }
