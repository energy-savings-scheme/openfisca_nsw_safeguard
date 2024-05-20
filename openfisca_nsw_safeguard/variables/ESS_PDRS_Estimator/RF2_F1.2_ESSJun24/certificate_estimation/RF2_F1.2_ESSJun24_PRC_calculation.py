from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class RF2_F1_2_ESSJun24_baseline_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      total_energy_consumption = buildings('RF2_F1_2_ESSJun24_total_energy_consumption', period)
      af = buildings('RF2_F1_2_ESSJun24_af', period)
      baseline_EEI = buildings('RF2_F1_2_ESSJun24_baseline_EEI', period)
      product_EEI = buildings('RF2_F1_2_ESSJun24_product_EEI', period)
      
      baseline_input_power = np.select(
          [
            product_EEI == 0, product_EEI != 0
          ], 
         [
              0, np.multiply((total_energy_consumption * af), (baseline_EEI / product_EEI) / 24)
          ])
      
      return baseline_input_power
  
  
class RF2_F1_2_ESSJun24_peak_demand_savings_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      baseline_peak_adjustment_factor = buildings('RF2_F1_2_ESSJun24_baseline_peak_adjustment_factor', period)
      baseline_input_power = buildings('RF2_F1_2_ESSJun24_baseline_input_power', period)
      input_power = buildings('RF2_F1_2_ESSJun24_input_power', period)
      firmness_factor = 1

      peak_demand_savings_capacity = ((baseline_input_power * baseline_peak_adjustment_factor)
                                        - (input_power * baseline_peak_adjustment_factor )) * firmness_factor
      return peak_demand_savings_capacity
  

class RF2_F1_2_ESSJun24ProductClass(Enum):
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


class RF2_F1_2_ESSJun24_product_class_peak_savings(Variable):
    value_type = Enum
    entity = Building
    definition_period = ETERNITY
    possible_values = RF2_F1_2_ESSJun24ProductClass
    default_value = RF2_F1_2_ESSJun24ProductClass.product_class_one
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


class RF2_F1_2_ESSJun24_duty_class_peak_savings(Variable):
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


class RF2_F1_2_ESSJun24_product_type_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = RCProductType
    default_value = RCProductType.integral_RDC
    definition_period = ETERNITY    
    metadata = {
      "label": 'Product Type for the refrigerated cabinet',
      "variable-type": "output",
    }


class RF2_F1_2_ESSJun24_peak_demand_annual_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Peak demand annual savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
         #product class
        product_class_savings = buildings('RF2_F1_2_ESSJun24_product_class', period)
        
        product_class_savings = np.select([
            product_class_savings == 'Class 1',
            product_class_savings == 'Class 2',
            product_class_savings == 'Class 3',
            product_class_savings == 'Class 4',
            product_class_savings == 'Class 5',
            product_class_savings == 'Class 6',
            product_class_savings == 'Class 7',
            product_class_savings == 'Class 8',
            product_class_savings == 'Class 9',
            product_class_savings == 'Class 10',
            product_class_savings == 'Class 11',
            product_class_savings == 'Class 12',
            product_class_savings == 'Class 13',
            product_class_savings == 'Class 14',
            product_class_savings == 'Class 15',
        ], 
        [
            RF2_F1_2_ESSJun24ProductClass.product_class_one,
            RF2_F1_2_ESSJun24ProductClass.product_class_two,
            RF2_F1_2_ESSJun24ProductClass.product_class_three,
            RF2_F1_2_ESSJun24ProductClass.product_class_four,
            RF2_F1_2_ESSJun24ProductClass.product_class_five,
            RF2_F1_2_ESSJun24ProductClass.product_class_six,
            RF2_F1_2_ESSJun24ProductClass.product_class_seven,
            RF2_F1_2_ESSJun24ProductClass.product_class_eight,
            RF2_F1_2_ESSJun24ProductClass.product_class_nine,
            RF2_F1_2_ESSJun24ProductClass.product_class_ten,
            RF2_F1_2_ESSJun24ProductClass.product_class_eleven,
            RF2_F1_2_ESSJun24ProductClass.product_class_twelve,
            RF2_F1_2_ESSJun24ProductClass.product_class_thirteen,
            RF2_F1_2_ESSJun24ProductClass.product_class_fourteen,
            RF2_F1_2_ESSJun24ProductClass.product_class_fifteen         
      ])
        
        #duty class
        duty_type = buildings('RF2_F1_2_ESSJun24_duty_class', period)
    
        #product type
        is_integral_RDC = (
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_one) +
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_two) +
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_seven) +
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_eight) +
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_eleven)
                            )

        is_integral_ice_cream_freezer_cabinet = (
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_five)
        )

        is_remote_RDC = (
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_twelve) +
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_thirteen) +
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_fourteen) +
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_fifteen)
        )

        is_gelato_or_icecream_scooping_cabinets = (
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_six)
        )

        is_RSC = (
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_three) +
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_four) +
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_nine) +
                            (product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_ten)
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
        usage_factor = 1
        temperature_factor = parameters(period).PDRS.refrigerated_cabinets.table_RF2_2_ESSJun24['temperature_factor'][product_type][duty_type]
        
        baseline_peak_adjustment_factor = temperature_factor * usage_factor

        #af
        af = parameters(period).PDRS.refrigerated_cabinets.table_RF2_1_ESSJun24['adjustment_factor'][product_class_savings][duty_type]

        #tec
        total_energy_consumption = buildings('RF2_F1_2_ESSJun24_total_energy_consumption', period)

        #baseline EEI
        baseline_EEI = parameters(period).PDRS.refrigerated_cabinets.table_RF2_1_ESSJun24['baseline_EEI'][product_class_savings][duty_type],
            
        #product EEI
        product_EEI = buildings('RF2_F1_2_ESSJun24_product_EEI', period)

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

        #lifetime_by_rc_class        
        product_class_savings = np.select([
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_one,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_two,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_three,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_four,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_five,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_six,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_seven,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_eight,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_nine,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_ten,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_eleven,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_twelve,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_thirteen,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_fourteen,
            product_class_savings == RF2_F1_2_ESSJun24ProductClass.product_class_fifteen
        ],
        [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
        ])

        #lifetime
        product_class = buildings('RF2_F1_2_ESSJun24_product_class_int', period)     
        lifetime_by_rc_class = np.select(
            [
                (product_class >= 1) * (product_class <= 11),
                (product_class >= 12) * (product_class <= 15)
            ],
            [
                8,
                12
            ])

        #peak demand reduction capacity
        summer_peak_demand_reduction_duration = 6

        peak_demand_annual_savings = peak_demand_savings_capacity * summer_peak_demand_reduction_duration * lifetime_by_rc_class

        peak_demand_annual_savings_return = np.select([
                peak_demand_annual_savings <= 0, peak_demand_annual_savings > 0
            ], 
	        [
                0, peak_demand_annual_savings
            ])

        return peak_demand_annual_savings_return


class RF2_F1_2_ESSJun24_peak_demand_reduction_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Input Factor'
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      peak_demand_savings_capacity = buildings('RF2_F1_2_ESSJun24_peak_demand_savings_capacity', period)
      summer_peak_demand_reduction_duration = 6
      lifetime = buildings('RF2_F1_2_ESSJun24_lifetime_by_rc_class', period)

      return peak_demand_savings_capacity * summer_peak_demand_reduction_duration * lifetime


class RF2_F1_2_ESSJun24_baseline_peak_adjustment_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Adjustment Factor'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
      product_type = buildings('RF2_F1_2_ESSJun24_product_type', period)
      duty_type = buildings('RF2_F1_2_ESSJun24_duty_class', period)
      usage_factor = 1
      
      temperature_factor = parameters(period).PDRS.refrigerated_cabinets.table_RF2_2_ESSJun24['temperature_factor'][product_type][duty_type]
      
      baseline_peak_adjustment_factor = temperature_factor * usage_factor
      return baseline_peak_adjustment_factor
  
  
class RF2_F1_2_ESSJun24_PRC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'label' : 'The number of PRCs for RF2_F1_2_ESSJun24',
        'variable-type' : 'output'
    }

    def formula(buildings, period, parameters):
        peak_demand_capacity = buildings('RF2_F1_2_ESSJun24_peak_demand_reduction_capacity', period)
        network_loss_factor = buildings('RF2_F1_2_ESSJun24_get_network_loss_factor_by_postcode', period)
        kw_to_0_1kw = 10
        replacement_activity = buildings('RF2_F1_2_ESSJun24_replacement_activity', period)
        EEI_eligible_replacement = buildings('RF2_F1_2_ESSJun24_product_minimum_EEI_eligibility', period)
        RF2_F1_2_ESSJun24_eligible_PRCs = np.select(
            [
                replacement_activity * EEI_eligible_replacement,
                replacement_activity * np.logical_not(EEI_eligible_replacement),
                np.logical_not(replacement_activity) * EEI_eligible_replacement,
                np.logical_not(replacement_activity) * np.logical_not(EEI_eligible_replacement)
            ],
            [
                (peak_demand_capacity * network_loss_factor * kw_to_0_1kw),
                0,
                0,
                0
            ])
        
        result_to_return = np.select(
            [
                RF2_F1_2_ESSJun24_eligible_PRCs <= 0, RF2_F1_2_ESSJun24_eligible_PRCs > 0
            ],
            [
                0, RF2_F1_2_ESSJun24_eligible_PRCs
            ])
        return result_to_return