from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class RF2_F1_2_ESSJun24_input_power(Variable):
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

      input_power = (total_energy_consumption * af) / 24
      return input_power


class RF2_F1_2_ESSJun24_lifetime_by_rc_class(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
 
    def formula(buildings, period, parameters):
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

        return lifetime_by_rc_class


class RF2_F1_2_ESSJun24_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        'variable-type': 'output'
    }

    def formula(buildings, period, parameters):
      total_energy_consumption = buildings('RF2_F1_2_ESSJun24_total_energy_consumption', period)
      baseline_EEI = buildings('RF2_F1_2_ESSJun24_baseline_EEI', period)
      product_EEI = buildings('RF2_F1_2_ESSJun24_product_EEI', period)
      af = buildings('RF2_F1_2_ESSJun24_af', period)
      lifetime_by_rc_class = buildings('RF2_F1_2_ESSJun24_lifetime_by_rc_class', period)
      
      deemed_electricity_savings = np.multiply(total_energy_consumption * (baseline_EEI / product_EEI - 1) * af * 365, (lifetime_by_rc_class / 1000))
      return deemed_electricity_savings
    

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


class RF2_F1_2_ESSJun24_product_class_savings(Variable):
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


class RCDutyClass_savings(Enum):
    heavy_duty = 'Heavy duty'
    normal_duty = 'Normal duty'
    light_duty = 'Light duty'


class RF2_F1_2_ESSJun24_duty_class_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = RCDutyClass_savings
    default_value = RCDutyClass_savings.normal_duty
    definition_period = ETERNITY
    metadata = {
      'variable-type' : 'user-input',
      'label' : 'Duty Classification',
      'display_question' : 'Duty Classification for refrigerated cabinet',
      'sorting' : 4
    }


class RF2_F1_2_ESSJun24_annual_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
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

        #af
        af = parameters(period).ESS.HEAB.table_F1_2_1_ESSJun24['adjustment_factor'][product_class_savings][duty_type],

        #tec
        total_energy_consumption = buildings('RF2_F1_2_ESSJun24_total_energy_consumption', period)

        #baseline EEI
        baseline_EEI = parameters(period).ESS.HEAB.table_F1_2_1_ESSJun24['baseline_EEI'][product_class_savings][duty_type]

        #product EEI
        product_EEI = buildings('RF2_F1_2_ESSJun24_product_EEI', period)

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
      
        #deemed electricity savings
        deemed_electricity_savings = np.multiply(total_energy_consumption * (baseline_EEI / product_EEI - 1) * af * 365, (lifetime_by_rc_class / 1000))

        #regional network factor
        postcode = buildings('RF2_F1_2_ESSJun24_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        regional_network_factor = rnf.calc(postcode) 

        #electricity savings
        annual_energy_savings = deemed_electricity_savings * regional_network_factor

        annual_savings_return = np.select([
            annual_energy_savings <= 0, annual_energy_savings > 0
        ], 
	    [
            0, annual_energy_savings
        ])
        return annual_savings_return
    

class RF2_F1_2_ESSJun24_PDRS__regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'
    metadata = {
        'variable-type': 'inter-interesting',
        'alias':'PDRS Regional Network Factor',
        'display_question': 'PDRS regional network factor'
    }

    def formula(buildings, period, parameters):
        postcode = buildings('RF2_F1_2_ESSJun24_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode) 


class RF2_F1_2_ESSJun24_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'RF2_F1_2_ESSJun24 Electricity savings'
    metadata = {
        'alias': 'RF2_F1_2_ESSJun24 electricity savings',
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('RF2_F1_2_ESSJun24_deemed_activity_electricity_savings', period)   
        regional_network_factor = buildings('RF2_F1_2_ESSJun24_PDRS__regional_network_factor', period)

        electricity_savings = deemed_electricity_savings * regional_network_factor
        return electricity_savings
  

class RF2_F1_2_ESSJun24_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for HVAC1'

    def formula(buildings, period, parameters):
      electricity_savings = buildings('RF2_F1_2_ESSJun24_electricity_savings', period)
      electricity_certificate_conversion_factor = 1.06
      replacement_activity = buildings('RF2_F1_2_ESSJun24_replacement_activity', period)
      EEI_eligible_replacement = buildings('RF2_F1_2_ESSJun24_product_minimum_EEI_eligibility', period)

      RF2_F1_2_ESSJun24_eligible_ESCs = np.select(
            [
                replacement_activity * EEI_eligible_replacement,
                replacement_activity * np.logical_not(EEI_eligible_replacement),
                np.logical_not(replacement_activity) * EEI_eligible_replacement,
                np.logical_not(replacement_activity) * np.logical_not(EEI_eligible_replacement)
            ],
            [
                (electricity_savings * electricity_certificate_conversion_factor),
                0,
                0,
                0
            ])

      result_to_return = np.select([
                RF2_F1_2_ESSJun24_eligible_ESCs <= 0, RF2_F1_2_ESSJun24_eligible_ESCs > 0
            ],
            [
                0, RF2_F1_2_ESSJun24_eligible_ESCs
            ])
      return result_to_return