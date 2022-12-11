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
    "variable-type": "user-input",
    "label": "Total Energy Consumption",
    "display_question": "Total Energy Consumption",
    "sorting": 6
  }
  

class RF2_total_display_area(Variable):
  value_type = float
  entity = Building
  definition_period = ETERNITY
  metadata = {
    "variable-type": "user-input",
    "label": "Total display area",
    "display_question": "Total display area",
    "sorting": 7
  }


class RF2_af(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Adjustment factor"

    def formula(buildings, period, parameters):
      product_class = buildings('RF2_product_class', period)
      duty_type = buildings('RF2_duty_class', period)
      new_equipment = buildings('RF2_replacement_activity', period)
    
      product_class = np.select([
          product_class == 'Class 1',
          product_class == 'Class 2',
          product_class == 'Class 3',
          product_class == 'Class 4',
          product_class == 'Class 5',
          product_class == 'Class 6',
          product_class == 'Class 7',
          product_class == 'Class 8',
          product_class == 'Class 9',
          product_class == 'Class 10',
          product_class == 'Class 11',
          product_class == 'Class 12',
          product_class == 'Class 13',
          product_class == 'Class 14',
          product_class == 'Class 15',
        ], 
        [
          RF2ProductClass.product_class_one,
          RF2ProductClass.product_class_two,
          RF2ProductClass.product_class_three,
          RF2ProductClass.product_class_four,
          RF2ProductClass.product_class_five,
          RF2ProductClass.product_class_six,
          RF2ProductClass.product_class_seven,
          RF2ProductClass.product_class_eight,
          RF2ProductClass.product_class_nine,
          RF2ProductClass.product_class_ten,
          RF2ProductClass.product_class_eleven,
          RF2ProductClass.product_class_twelve,
          RF2ProductClass.product_class_thirteen,
          RF2ProductClass.product_class_fourteen,
          RF2ProductClass.product_class_fifteen         
        ])
      
      af = np.select(
        [ 
          new_equipment, 
          np.logical_not(new_equipment)
        ],
        [ 
          parameters(period).ESS.HEAB.table_F1_1_1['adjustment_factor'][product_class][duty_type],
          parameters(period).PDRS.refrigerated_cabinets.table_RF2_1['adjustment_factor'][product_class][duty_type]
        ]
      )
      return af
    
    
class RF2_baseline_EEI(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Baseline EEI"
  
    def formula(buildings, period, parameters):
      product_class = buildings('RF2_product_class', period)
      duty_type = buildings('RF2_duty_class', period)
      replacement_activity = buildings('RF2_replacement_activity', period)
    
      product_class = np.select([
          product_class == 'Class 1',
          product_class == 'Class 2',
          product_class == 'Class 3',
          product_class == 'Class 4',
          product_class == 'Class 5',
          product_class == 'Class 6',
          product_class == 'Class 7',
          product_class == 'Class 8',
          product_class == 'Class 9',
          product_class == 'Class 10',
          product_class == 'Class 11',
          product_class == 'Class 12',
          product_class == 'Class 13',
          product_class == 'Class 14',
          product_class == 'Class 15',
        ], 
        [
          RF2ProductClass.product_class_one,
          RF2ProductClass.product_class_two,
          RF2ProductClass.product_class_three,
          RF2ProductClass.product_class_four,
          RF2ProductClass.product_class_five,
          RF2ProductClass.product_class_six,
          RF2ProductClass.product_class_seven,
          RF2ProductClass.product_class_eight,
          RF2ProductClass.product_class_nine,
          RF2ProductClass.product_class_ten,
          RF2ProductClass.product_class_eleven,
          RF2ProductClass.product_class_twelve,
          RF2ProductClass.product_class_thirteen,
          RF2ProductClass.product_class_fourteen,
          RF2ProductClass.product_class_fifteen         
        ])

      baseline_EEI = np.select(
        [ 
          replacement_activity,
          np.logical_not(replacement_activity)
        ],
        [ 
          parameters(period).PDRS.refrigerated_cabinets.table_RF2_1['baseline_EEI'][product_class][duty_type],
          parameters(period).ESS.HEAB.table_F1_1_1['baseline_EEI'][product_class][duty_type]
        ]
      )    
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
    product_class_one = 'Class 1'
    product_class_two = 'Class 2'
    product_class_three = 'Class 3'
    product_class_four = 'Class 4'
    product_class_five = 'Class 5'
    product_class_six = 'Class 6'
    product_class_seven = 'Class 7'
    product_class_eight = 'Class 8'
    product_class_nine = 'Class 9'
    product_class_ten = 'Class 10'
    product_class_eleven = 'Class 11'
    product_class_twelve = 'Class 12'
    product_class_thirteen = 'Class 13'
    product_class_fourteen = 'Class 14'
    product_class_fifteen = 'Class 15'


class RF2_product_class(Variable):
    value_type = str
    entity = Building
    default_value = 'Class 1'
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
      
      product_class = np.select([
        product_class == 'Class 1',
        product_class == 'Class 2',
        product_class == 'Class 3',
        product_class == 'Class 4',
        product_class == 'Class 5',
        product_class == 'Class 6',
        product_class == 'Class 7',
        product_class == 'Class 8',
        product_class == 'Class 9',
        product_class == 'Class 10',
        product_class == 'Class 11',
        product_class == 'Class 12',
        product_class == 'Class 13',
        product_class == 'Class 14',
        product_class == 'Class 15',
      ], 
      [
        RF2ProductClass.product_class_one,
        RF2ProductClass.product_class_two,
        RF2ProductClass.product_class_three,
        RF2ProductClass.product_class_four,
        RF2ProductClass.product_class_five,
        RF2ProductClass.product_class_six,
        RF2ProductClass.product_class_seven,
        RF2ProductClass.product_class_eight,
        RF2ProductClass.product_class_nine,
        RF2ProductClass.product_class_ten,
        RF2ProductClass.product_class_eleven,
        RF2ProductClass.product_class_twelve,
        RF2ProductClass.product_class_thirteen,
        RF2ProductClass.product_class_fourteen,
        RF2ProductClass.product_class_fifteen         
      ])
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
    integral_RDC = 'Integral refrigerated display cabinet'
    integral_ice_cream_freezer_cabinet = 'Integral ice cream freezer cabinet'
    remote_RDC = 'Remote refrigerated display cabinet'
    gelato_ice_cream_scooping_cabinet = 'Gelato or ice cream scooping cabinet'
    RSC = 'Refrigerated storage cabinet'


class RF2_product_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = RCProductType
    default_value = RCProductType.integral_RDC
    definition_period = ETERNITY    
    metadata = {
      "label": 'Product Type for the refrigerated cabinet',
      # "display_question":  "What is the product type for the refrigerated cabinet?",
      "variable-type": "output",
    }
    
    def formula(buildings, period, parameters):
      product_class = buildings('RF2_product_class', period)

      product_class = np.select([
        product_class == 'Class 1',
        product_class == 'Class 2',
        product_class == 'Class 3',
        product_class == 'Class 4',
        product_class == 'Class 5',
        product_class == 'Class 6',
        product_class == 'Class 7',
        product_class == 'Class 8',
        product_class == 'Class 9',
        product_class == 'Class 10',
        product_class == 'Class 11',
        product_class == 'Class 12',
        product_class == 'Class 13',
        product_class == 'Class 14',
        product_class == 'Class 15',
      ], 
      [
        RF2ProductClass.product_class_one,
        RF2ProductClass.product_class_two,
        RF2ProductClass.product_class_three,
        RF2ProductClass.product_class_four,
        RF2ProductClass.product_class_five,
        RF2ProductClass.product_class_six,
        RF2ProductClass.product_class_seven,
        RF2ProductClass.product_class_eight,
        RF2ProductClass.product_class_nine,
        RF2ProductClass.product_class_ten,
        RF2ProductClass.product_class_eleven,
        RF2ProductClass.product_class_twelve,
        RF2ProductClass.product_class_thirteen,
        RF2ProductClass.product_class_fourteen,
        RF2ProductClass.product_class_fifteen         
      ])

      is_integral_RDC = (
                          (product_class == RF2ProductClass.product_class_one) +
                          (product_class == RF2ProductClass.product_class_two) +
                          (product_class == RF2ProductClass.product_class_seven) +
                          (product_class == RF2ProductClass.product_class_eight) +
                          (product_class == RF2ProductClass.product_class_eleven)
                          )

      is_integral_ice_cream_freezer_cabinet = (
                          (product_class == RF2ProductClass.product_class_five)
      )

      is_remote_RDC = (
                          (product_class == RF2ProductClass.product_class_twelve) +
                          (product_class == RF2ProductClass.product_class_thirteen) +
                          (product_class == RF2ProductClass.product_class_fourteen) +
                          (product_class == RF2ProductClass.product_class_fifteen)
      )

      is_gelato_or_icecream_scooping_cabinets = (
                          (product_class == RF2ProductClass.product_class_six)
      )

      is_RSC = (
                          (product_class == RF2ProductClass.product_class_three) +
                          (product_class == RF2ProductClass.product_class_four) +
                          (product_class == RF2ProductClass.product_class_nine) +
                          (product_class == RF2ProductClass.product_class_ten)
      )

      product_type = np.select(
                                  [
                                  is_integral_RDC,
                                  is_integral_ice_cream_freezer_cabinet,
                                  is_remote_RDC,
                                  is_gelato_or_icecream_scooping_cabinets,
                                  is_RSC
                                  ],
                                  [
                                      RCProductType.integral_RDC,
                                      RCProductType.integral_ice_cream_freezer_cabinet,
                                      RCProductType.remote_RDC,
                                      RCProductType.gelato_ice_cream_scooping_cabinet,
                                      RCProductType.RSC
                                  ]
                              )
      return product_type


class RCDutyClass(Enum):
    heavy_duty = 'Heavy duty'
    normal_duty = 'Normal duty'
    light_duty = 'Light duty'


class RF2_duty_class(Variable):
    value_type = Enum
    entity = Building
    possible_values = RCDutyClass
    default_value = RCDutyClass.normal_duty
    definition_period = ETERNITY
    label = 'What is the duty class for the refrigerated cabinet?'
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
    metadata = {
        'variable-type' : 'user-input',
        'alias' : 'PDRS Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1,
        'label': 'Postcode'
        }


class RF2_replacement_activity(Variable):  
    value_type = bool
    default_value = True
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Replacement or new installation activity',
        'display_question' : 'Is the activity a replacement of existing equipment?',
        'sorting' : 3
        }

class RF2_product_EEI_ESC_replacement_eligibility(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY

    def formula(building, period, parameters):
      product_EEI = building('RF2_product_EEI', period)
      product_class_5 = building('RF2_product_class', period)
        
      replace_product_EEI_to_check_ESC = np.select(
           [
              (product_EEI < 51),
              (product_EEI >= 51) * (product_EEI < 81) * (product_class_5 == 'Class 5'),
              (product_EEI >= 51) * (product_EEI < 81) * (product_class_5 != 'Class 5'),
              (product_EEI >= 81)
          ],
          [
              True,
              False,
              True,
              False
          ])
      return replace_product_EEI_to_check_ESC


class RF2_product_EEI_ESC_install_eligibility(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY

    def formula(building, period, parameters):
        product_EEI = building('RF2_product_EEI', period)
          
        install_product_EEI_to_check_ESC = np.select(
            [    
                product_EEI < 77,
                product_EEI >= 77
            ],
            [
                True,
                False
            ])
        return install_product_EEI_to_check_ESC


class RF2_product_EEI_PRC_replacement_eligibility(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY

    def formula(building, period, parameters):
        product_EEI = building('RF2_product_EEI', period)
        product_class_5 = building('RF2_product_class', period)
        
        product_EEI_to_check_PRC = np.select(
          [
              (product_EEI < 51),
              (product_EEI >= 51) * (product_EEI < 81) * (product_class_5 == 'Class 5'),
              (product_EEI >= 51) * (product_EEI < 81) * (product_class_5 != 'Class 5'),
              (product_EEI >= 81)
          ],
          [
              True,
              False,
              True,
              False
          ])
        return product_EEI_to_check_PRC