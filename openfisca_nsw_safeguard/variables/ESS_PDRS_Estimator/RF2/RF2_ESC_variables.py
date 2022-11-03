from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


""" Parameters for RF2 ESC Calculation
    These variables use GEMS Registry data
"""
class RF2_total_energy_consumption(Variable):
  #Total energy consumption
  reference = 'kWh per day'
  value_type = float
  entity = Building
  definition_period = ETERNITY
  metadata = {
    'variable-type': 'user-input',
    'label': 'TEC (kWh/day)',
    'display_question': 'Total Energy Consumption of the replacement refrigerated cabinet model as recorded in the GEMS Registry',
    'sorting' : 5
  }
  

class RF2_total_display_area(Variable):
  value_type = float
  entity = Building
  definition_period = ETERNITY
  metadata = {
    'variable-type': 'user-input',
    'label': 'Display Area',
    'display_question': 'Total Display Area of the refrigerated cabinet(m2)',
    'sorting' : 7
  }


class RF2_af(Variable):
  value_type = float
  entity = Building
  definition_period = ETERNITY
  label = "Adjustment factor"

  def formula(buildings, period, parameters):
    product_class = buildings('RF2_product_class', period)
    duty_type = buildings('RF2_duty_class', period)
    
    af = parameters(period).PDRS.refrigerated_cabinets.table_RF2_1['adjustment_factor'][product_class][duty_type]
    return af


class RF2_baseline_EEI(Variable):
  value_type = float
  entity = Building
  definition_period = ETERNITY
  label = "Baseline EEI"
  
  def formula(buildings, period, parameters):
    product_class = buildings('RF2_product_class', period)
    duty_type = buildings('RF2_duty_class', period)
    
    baseline_EEI = parameters(period).PDRS.refrigerated_cabinets.table_RF2_1['baseline_EEI'][product_class][duty_type]
    
    return baseline_EEI


class RF2_product_EEI(Variable):
  value_type = float
  entity = Building
  definition_period = ETERNITY
  metadata = {
    'variable-type' : 'user-input',
    'label' : 'Product EEI',
    'display_question' : 'Energy Efficiency Index of the replacement refrigerated cabinet model as recorded in the GEMS Registry',
    'sorting' : 8
  }
  
  
class RF2ProductClass(Enum):
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


class RF2_product_class(Variable):
    value_type = Enum
    entity = Building
    possible_values = RF2ProductClass
    default_value = RF2ProductClass.product_class_one
    definition_period = ETERNITY
    label = 'What is the product class for the refrigerated cabinet?'
    metadata = {
      'variable-type': 'user-input',
      'label': 'Product Class',
      'display_question': 'Refrigerated Cabinet Product Class (Product Characteristics Code)',
      'sorting' : 6
    }


class RF2_product_class_int(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      product_class = buildings('RF2_product_class', period)
      product_class_int = np.select([
        product_class == RF2ProductClass.product_class_one,
        product_class == RF2ProductClass.product_class_two,
        product_class == RF2ProductClass.product_class_three,
        product_class == RF2ProductClass.product_class_four,
        product_class == RF2ProductClass.product_class_five,
        product_class == RF2ProductClass.product_class_six,
        product_class == RF2ProductClass.product_class_seven,
        product_class == RF2ProductClass.product_class_eight,
        product_class == RF2ProductClass.product_class_nine,
        product_class == RF2ProductClass.product_class_ten,
        product_class == RF2ProductClass.product_class_eleven,
        product_class == RF2ProductClass.product_class_twelve,
        product_class == RF2ProductClass.product_class_thirteen,
        product_class == RF2ProductClass.product_class_fourteen,
        product_class == RF2ProductClass.product_class_fifteen
      ],
      [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
      ]
      )
      
      return product_class_int

      
class RCProductType(Enum):
    integral_RDC = 'Product is an integral refrigerated display cabinet.'
    integral_ice_cream_freezer_cabinet = 'Product is an integral ice cream freezer cabinet.'
    remote_RDC = 'Product is a remote refrigerated display cabinet.'
    gelato_ice_cream_scooping_cabinet = 'Product is a gelato or ice cream scooping cabinet.'
    RSC = 'Product is a refrigerated storage cabinet.'


class RF2_product_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = RCProductType
    default_value = RCProductType.integral_RDC
    definition_period = ETERNITY
    label = 'What is the product type for the refrigerated cabinet?'
    metadata = {   
      'variable-type': 'user-input'
    }


class RCDutyClass(Enum):
    heavy_duty = 'Product is a heavy duty refrigerated cabinet.'
    normal_duty = 'Product is a normal duty refrigerated cabinet.'
    light_duty = 'Product is a light duty refrigerated cabinet.'


class RF2_duty_class(Variable):
    value_type = Enum
    entity = Building
    possible_values = RCDutyClass
    default_value = RCDutyClass.normal_duty
    definition_period = ETERNITY
    metadata = {
      'variable-type' : 'user-input',
      'label' : 'Duty Classification',
      'display_question' : 'Duty Classification for refrigerated cabinet',
      'sorting' : 4
    }


class RF2_PDRS__postcode(Variable):
    # this variable is used as the first input on all estimator certificate calculation pages
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = "What is the postcode for the building you are calculating PRCs for?"
    metadata={
        'variable-type' : 'user-input',
        'alias' : 'PDRS Postcode',
        'label' : 'Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1
        }


class RF2_New_Equipment(Variable):
    value_type = bool
    default_value = True
    entity = Building
    definition_period = ETERNITY
    label = 'New or Used equipment'
    metadata = {
        'variable-type': 'user-input',
        'label' : 'New or Used equipment',
        'display_question' : 'Is the end-user equipment a new commercial refrigerated cabinet?',
        'sorting' : 3
        }