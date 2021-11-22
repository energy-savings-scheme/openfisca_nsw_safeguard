from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


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
