from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class RF2_baseline_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      total_energy_consumption = buildings('RF2_total_energy_consumption', period)
      af = buildings('RF2_af', period)
      baseline_EEI = buildings('RF2_baseline_EEI', period)
      product_EEI = buildings('RF2_product_EEI', period)
      
      baseline_input_power = np.select(
          [
            product_EEI == 0, product_EEI != 0
          ], 
         [
              0, np.multiply((total_energy_consumption * af), (baseline_EEI / product_EEI) / 24)
          ])
      
      return baseline_input_power
  
  
class RF2_peak_demand_savings_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      baseline_peak_adjustment_factor = buildings('RF2_baseline_peak_adjustment_factor', period)
      baseline_input_power = buildings('RF2_baseline_input_power', period)
      input_power = buildings('RF2_input_power', period)
      firmness_factor = 1

      peak_demand_savings_capacity = ((baseline_input_power * baseline_peak_adjustment_factor)
                                        - (input_power * baseline_peak_adjustment_factor )) * firmness_factor
      return peak_demand_savings_capacity
  

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


class RF2_product_class_peak_savings(Variable):
    value_type = Enum
    entity = Building
    definition_period = ETERNITY
    possible_values = RF2ProductClass
    default_value = RF2ProductClass.product_class_one
    metadata = {
      'variable-type': 'user-input',
      'label': 'Product Class',
      'display_question': 'Refrigerated Cabinet Product Class (Product Characteristics Code)',
      'sorting' : 6
    }


class RCDutyClass_peak_savings(Enum):
    heavy_duty = 'Heavy duty'
    normal_duty = 'Normal duty'
    light_duty = 'Light duty'


class RF2_duty_class_peak_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = RCDutyClass_peak_savings
    default_value = RCDutyClass_peak_savings.normal_duty
    definition_period = ETERNITY
    metadata = {
      'variable-type' : 'user-input',
      'label' : 'Duty Classification',
      'display_question' : 'Duty Classification for refrigerated cabinet',
      'sorting' : 4
    }


class RCProductType(Enum):
    integral_RDC = 'Integral refrigerated display cabinet'
    integral_ice_cream_freezer_cabinet = 'Integral ice cream freezer cabinet'
    remote_RDC = 'Remote refrigerated display cabinet'
    gelato_ice_cream_scooping_cabinet = 'Gelato or ice cream scooping cabinet'
    RSC = 'Refrigerated storage cabinet'


class RF2_product_type_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = RCProductType
    default_value = RCProductType.integral_RDC
    definition_period = ETERNITY    
    metadata = {
      "label": 'Product Type for the refrigerated cabinet',
      "variable-type": "output",
    }

class RF2_peak_demand_annual_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand annual savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
        #product class
        product_class = buildings('RF2_product_class', period)

        #duty class
        duty_type = buildings('RF2_duty_class', period)
        
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
        
        #product type
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
                                    ])

        #baseline peak adjustment factor
        print(product_type)
        print(duty_type)
        usage_factor = 1
        temperature_factor = parameters(period).PDRS.refrigerated_cabinets.table_RF2_2['temperature_factor'][product_type][duty_type]
        
        baseline_peak_adjustment_factor = temperature_factor * usage_factor

        #replacement activity
        replacement_activity = buildings('RF2_replacement_activity', period)

        #af
        af = np.select(
            [
                np.logical_not(replacement_activity), #new install
                replacement_activity
            ],
            [
                parameters(period).ESS.HEAB.table_F1_1_1['adjustment_factor'][product_class][duty_type],
                parameters(period).PDRS.refrigerated_cabinets.table_RF2_1['adjustment_factor'][product_class][duty_type]
            ])
        
        #tec
        total_energy_consumption = buildings('RF2_total_energy_consumption', period)

        #baseline EEI
        baseline_EEI = np.select(
            [
                replacement_activity,
                np.logical_not(replacement_activity) #new install
            ],
            [
                parameters(period).PDRS.refrigerated_cabinets.table_RF2_1['baseline_EEI'][product_class][duty_type],
                parameters(period).ESS.HEAB.table_F1_1_1['baseline_EEI'][product_class][duty_type]
            ])

        #product EEI
        product_EEI = buildings('RF2_product_EEI', period)

        #baseline input power
        baseline_input_power = np.select(
            [
                product_EEI == 0, product_EEI != 0
            ],
            [
                0, np.multiply((total_energy_consumption * af), (baseline_EEI / product_EEI) / 24)
            ])

        #input power
        input_power = (total_energy_consumption * af) / 24

        #firmness factor
        firmness_factor = 1

        #peak demand savings capacity
        peak_demand_savings_capacity = ((baseline_peak_adjustment_factor * baseline_input_power) - (input_power * baseline_peak_adjustment_factor )) * firmness_factor

        #peak demand annual savings
        summer_peak_demand_reduction_duration = 6

        peak_demand_annual_savings = peak_demand_savings_capacity * summer_peak_demand_reduction_duration
        return peak_demand_annual_savings


class RF2_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      peak_demand_savings_capacity = buildings('RF2_peak_demand_savings_capacity', period)
      summer_peak_demand_reduction_duration = 6
      lifetime = buildings('RF2_lifetime_by_rc_class', period)

      return peak_demand_savings_capacity * summer_peak_demand_reduction_duration * lifetime


class RF2_baseline_peak_adjustment_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Adjustment Factor'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
      product_type = buildings('RF2_product_type', period)
      duty_type = buildings('RF2_duty_class', period)
      usage_factor = 1
      
      temperature_factor = parameters(period).PDRS.refrigerated_cabinets.table_RF2_2['temperature_factor'][product_type][duty_type]
      
      baseline_peak_adjustment_factor = temperature_factor * usage_factor
      return baseline_peak_adjustment_factor
  
  
class RF2_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'label' : 'The number of PRCs for RF2',
        'variable-type' : 'output'
    }

    def formula(buildings, period, parameters):
        peak_demand_capacity = buildings('RF2_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('RF2_get_network_loss_factor_by_postcode', period)
        kw_to_0_1kw = 10
        replacement_activity = buildings('RF2_replacement_activity', period)
        EEI_eligible_replacement = buildings('RF2_product_EEI_PRC_replacement_eligibility', period)
        EEI_eligible_install = buildings('RF2_product_EEI_ESC_install_eligibility', period)
        RF2_eligible_PRCs = np.select(
            [
                replacement_activity * EEI_eligible_replacement,
                np.logical_not(replacement_activity) * np.logical_not(EEI_eligible_replacement),
                replacement_activity * EEI_eligible_install,
                np.logical_not(replacement_activity) * EEI_eligible_install
            ],
            [
                (peak_demand_capacity * network_loss_factor * kw_to_0_1kw),
                0,
                0,
                0
            ])
        
        result_to_return = np.select(
            [
                RF2_eligible_PRCs <= 0, RF2_eligible_PRCs > 0
            ],
            [
                0, RF2_eligible_PRCs
            ])
        return result_to_return