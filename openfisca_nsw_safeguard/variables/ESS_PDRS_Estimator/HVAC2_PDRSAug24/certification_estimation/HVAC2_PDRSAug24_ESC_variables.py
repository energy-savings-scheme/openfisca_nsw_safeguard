import numpy as np
from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building


""" Parameters for HVAC2 ESC Calculation
    These variables use GEMS Registry data
"""
class HVAC2_PDRSAug24_heating_capacity_input(BaseVariable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Air Conditioner Heating Capacity",
        'display_question': 'Rated heating capacity at 7c as recorded in the GEMS Registry',
        'sorting' : 9,
        'label': 'Rated heating capacity (kW)'
    }


class HVAC2_PDRSAug24_cooling_capacity_input(BaseVariable):
    reference = 'unit in kw'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Air Conditioner Cooling Capacity",
        'display_question': 'Rated cooling capacity at 35c as recorded in the GEMS Registry',
        'label': 'Rated cooling capacity (kW)',
        'sorting' : 5
    }


class HVAC2_PDRSAug24_rated_ACOP_input(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Rated ACOP",
        'display_question': 'Annual Coefficient of Performance (ACOP) as defined in GEMS',
        'sorting' : 11,
        'label': 'Rated ACOP'
    }


class HVAC2_PDRSAug24_baseline_AEER_input(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "AEER",
        "variable-type": "output",
        "label": "Baseline AEER"
    }

    def formula(building, period, parameters):
        product_class = building('HVAC2_PDRSAug24_product_class', period)
        new_or_replacement_activity = building('HVAC2_PDRSAug24_Activity', period)
        baseline_aeer = parameters(period).ESS.HEAB.table_F4_2_product_class.AEER[new_or_replacement_activity][product_class]
        return baseline_aeer


class HVAC2_PDRSAug24_rated_AEER_input(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Rated AEER",
        "display_question": 'Annual Energy Efficiency Ratio as defined in GEMS',
        'sorting': 7,
        'label': 'Rated AEER'
    }
    
    
class HVAC2_PDRSAug24_certificate_climate_zone(BaseVariable):
    value_type = int
    entity = Building
    label = "Which climate zone is the End-User equipment installed in, as defined in ESS Table A27?"
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'inter-interesting'
    }
    
    def formula(building, period, parameters):
        postcode = building('HVAC2_PDRSAug24_PDRS__postcode', period)
        rnf = parameters(period).ESS.ESS_general.table_A27_4_climate_zone_by_postcode
        zone_int = rnf.calc(postcode)
        return zone_int


class HVAC2_PDRSAug24_get_climate_zone_by_postcode(BaseVariable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'inter-interesting',
        'alias': 'climate zone'
    }
    
    def formula(building, period, parameters):
        postcode = building('HVAC2_PDRSAug24_PDRS__postcode', period)
        rnf = parameters(period).ESS.ESS_general.table_A27_4_climate_zone_by_postcode
        zone_int = rnf.calc(postcode)
        climate_zone_str = np.select([zone_int == 1, zone_int == 2, zone_int == 3],
                                     ['hot', 'mixed', 'cold'])
        return climate_zone_str


class HVAC2_PDRSAug24_PDRS__postcode(BaseVariable):
    # using to get the climate zone
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata={
        'variable-type' : 'user-input',
        'alias' : 'PDRS Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1,
        'label': 'Postcode'
    }


class HVAC2ProductClass(Enum):
    product_class_5 = 'Class 5'
    product_class_6 = 'Class 6'
    product_class_7 = 'Class 7'
    product_class_8 = 'Class 8'
    product_class_9 = 'Class 9'
    product_class_10 = 'Class 10'
    product_class_11 = 'Class 11'
    product_class_12 = 'Class 12'
    product_class_18 = 'Class 18'
    product_class_19 = 'Class 19'
    product_class_20 = 'Class 20'
    product_class_21 = 'Class 21'
    product_class_24 = 'Class 24'
    product_class_25 = 'Class 25'
    product_class_27 = 'Class 27'


class HVAC2_PDRSAug24_product_class_input(BaseVariable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    metadata = {
      'variable-type': 'user-input',
      'label': 'Product Class',
      'display_question': 'Product class of the selected brand and model',
      'sorting' : 6
    }


class HVAC2_PDRSAug24_product_class(BaseVariable):
    value_type = str
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      product_class = buildings('HVAC2_PDRSAug24_product_class_input', period)
      product_class = np.select([
        product_class == HVAC2ProductClass.product_class_5.value,
        product_class == HVAC2ProductClass.product_class_6.value,
        product_class == HVAC2ProductClass.product_class_7.value,
        product_class == HVAC2ProductClass.product_class_8.value,
        product_class == HVAC2ProductClass.product_class_9.value,
        product_class == HVAC2ProductClass.product_class_10.value,
        product_class == HVAC2ProductClass.product_class_11.value,
        product_class == HVAC2ProductClass.product_class_12.value,
        product_class == HVAC2ProductClass.product_class_18.value,
        product_class == HVAC2ProductClass.product_class_19.value,
        product_class == HVAC2ProductClass.product_class_20.value,
        product_class == HVAC2ProductClass.product_class_21.value,
        product_class == HVAC2ProductClass.product_class_24.value,
        product_class == HVAC2ProductClass.product_class_25.value,
        product_class == HVAC2ProductClass.product_class_27.value,
      ], 
      [
        HVAC2ProductClass.product_class_5.name,    # returns 'product_class_5'
        HVAC2ProductClass.product_class_6.name,
        HVAC2ProductClass.product_class_7.name,
        HVAC2ProductClass.product_class_8.name,
        HVAC2ProductClass.product_class_9.name,
        HVAC2ProductClass.product_class_10.name,
        HVAC2ProductClass.product_class_11.name,
        HVAC2ProductClass.product_class_12.name,
        HVAC2ProductClass.product_class_18.name,
        HVAC2ProductClass.product_class_19.name,
        HVAC2ProductClass.product_class_20.name,
        HVAC2ProductClass.product_class_21.name,
        HVAC2ProductClass.product_class_24.name,
        HVAC2ProductClass.product_class_25.name,
        HVAC2ProductClass.product_class_27.name,
      ])
      return product_class


class HVAC2_PDRSAug24_product_class_int(BaseVariable):
    value_type = int
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      product_class = buildings('HVAC1_PDRSAug24_product_class_input', period)
      product_class_int = np.select([
        product_class == HVAC2ProductClass.product_class_5.value,
        product_class == HVAC2ProductClass.product_class_6.value,
        product_class == HVAC2ProductClass.product_class_7.value,
        product_class == HVAC2ProductClass.product_class_8.value,
        product_class == HVAC2ProductClass.product_class_9.value,
        product_class == HVAC2ProductClass.product_class_10.value,
        product_class == HVAC2ProductClass.product_class_11.value,
        product_class == HVAC2ProductClass.product_class_12.value,
        product_class == HVAC2ProductClass.product_class_18.value,
        product_class == HVAC2ProductClass.product_class_19.value,
        product_class == HVAC2ProductClass.product_class_20.value,
        product_class == HVAC2ProductClass.product_class_21.value,
        product_class == HVAC2ProductClass.product_class_24.value,
        product_class == HVAC2ProductClass.product_class_25.value,
        product_class == HVAC2ProductClass.product_class_27.value,
      ], 
      [ 5, 6, 7, 8, 9, 10, 11, 12, 18, 19, 20, 21, 24, 25, 27, ],
      default=0)
      return product_class_int


class HVAC2_PDRSAug24_commercial_THEC(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY 
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'THEC (kWh/year)',
        'display_question' : 'The total annual heating energy consumption of the new air conditioner',
        'sorting' : 10
    }


class HVAC2_PDRSAug24_equivalent_heating_hours_input(BaseVariable):
    reference = 'unit in hours per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }
    
    def formula(building, period, parameters):
        climate_zone = building('HVAC2_PDRSAug24_certificate_climate_zone', period)
        climate_zone_str = np.select([climate_zone == 1, climate_zone == 2, climate_zone == 3],
                                     ['hot_zone', 'average_zone', 'cold_zone'])
        heating_hours = parameters(period).ESS.HEAB.table_F4_1.equivalent_heating_hours[climate_zone_str]
        return heating_hours


class HVAC2_PDRSAug24_commercial_TCEC(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY 
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'TCEC (kWh/year)',
        'display_question' : 'The total annual cooling energy consumption of the new air conditioner',
        'sorting' : 6
    }


class HVAC2_PDRSAug24_equivalent_cooling_hours_input(BaseVariable):
    reference = 'unit in hours per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(building, period, parameters):
        climate_zone = building('HVAC2_PDRSAug24_certificate_climate_zone', period)
        climate_zone_str = np.select([climate_zone == 1, climate_zone == 2, climate_zone == 3],
                                     ['hot_zone', 'average_zone', 'cold_zone'])
        cooling_hours = parameters(period).ESS.HEAB.table_F4_1.equivalent_cooling_hours[climate_zone_str]
        return cooling_hours


class HVAC2_PDRSAug24_baseline_ACOP_input(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY

    def formula(building, period, parameters):
        product_class = building('HVAC2_PDRSAug24_product_class', period)
        new_or_replacement_activity = building('HVAC2_PDRSAug24_Activity', period)
        baseline_acop = parameters(period).ESS.HEAB.table_F4_2_product_class.ACOP[new_or_replacement_activity][product_class]
        return baseline_acop


class HVAC2_PDRSAug24_AC_Type(Enum):
    non_ducted_single_split_system = 'Non-ducted single split system'
    ducted_single_split_system = 'Ducted single split system'
    non_ducted_multi_split_system = 'Non-ducted multi-split system'
    ducted_multi_split_system = 'Ducted multi-split system'
    non_ducted_unitary_system = 'Non-ducted unitary system'
    ducted_unitary_system = 'Ducted unitary system'


class HVAC2_PDRSAug24_Air_Conditioner_type(BaseVariable):
    value_type = Enum
    entity = Building
    possible_values = HVAC2_PDRSAug24_AC_Type
    default_value = HVAC2_PDRSAug24_AC_Type.non_ducted_single_split_system
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label': 'Air conditioner type',
        'display_question' : 'What is your air conditioner type?',
        'sorting' : 4
    }


class HVAC2_PDRSAug24_Activity_Type(Enum):
    new_installation_activity = 'Installation of a new air conditioner'
    replacement_activity = 'Replacement of an existing air conditioner'



class HVAC2_PDRSAug24_Activity(BaseVariable):
    value_type = Enum
    entity = Building
    possible_values = HVAC2_PDRSAug24_Activity_Type
    default_value = HVAC2_PDRSAug24_Activity_Type.replacement_activity
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label': 'Replacement or new installation activity',
        'display_question' : 'Which one of the following activities are you implementing?',
        'sorting' : 3
    }


class HVAC2_PDRSAug24_TCSPF_mixed(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'user-input',
        'alias':  'Air Conditioner TCSPF',
        'label': 'Mixed TCSPF',
        'display_question': 'Total cooling season performance factor in an average climate zone',
        'sorting' : 8
    }


class HVAC2_PDRSAug24_TCSPF_or_AEER_exceeds_ESS_benchmark(BaseVariable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'alias':  'Air Conditioner has at least 5 years of Warranty'
    }

    def formula(buildings, period, parameters):
        AC_TCSPF = buildings('HVAC2_PDRSAug24_TCSPF_mixed', period)
        AC_AEER = buildings('HVAC2_PDRSAug24_rated_AEER_input', period)
        product_class = buildings('HVAC2_PDRSAug24_product_class', period)
        old_product_class = buildings('HVAC2_PDRSAug24_Air_Conditioner_type', period)
        TCSPF_is_zero = ((AC_TCSPF == 0) + (AC_TCSPF == None))
        AC_exceeds_cooling_benchmark = np.where(
            TCSPF_is_zero,
            (AC_AEER >= parameters(period).PDRS.AC.table_HVAC_2_2_product_class['AEER'][product_class]),
            (AC_TCSPF >= parameters(period).PDRS.AC.table_HVAC_2_2_product_class['TCSPF_mixed'][product_class])
            )
        return AC_exceeds_cooling_benchmark


class HVAC2_PDRSAug24_HSPF_mixed(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'alias':  'Air Conditioner HSPF mixed',
        'label': 'Mixed HSPF',
        'display_question': 'Heating seasonal performance factor in an average climate zone'
    }


class HVAC2_PDRSAug24_HSPF_cold(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'alias':  'Air Conditioner HSPF cold',
        'label': 'Cold HSPF',
        'display_question': 'Heating seasonal performance factor in a cold climate zone'
    }

class HVAC2_PDRSAug24_HSPF_or_ACOP_exceeds_ESS_benchmark(BaseVariable):
    """ This variable is used if the AC climate zone is hot or average and there is a GEMS heating capacity
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'alias':  'ESS - HSPF or ACOP exceeds benchmark'
    }

    def formula(buildings, period, parameters):
        AC_HSPF_mixed = buildings('HVAC2_PDRSAug24_HSPF_mixed', period)
        AC_HSPF_cold = buildings('HVAC2_PDRSAug24_HSPF_cold', period)
        AC_ACOP = buildings('HVAC2_PDRSAug24_rated_ACOP_input', period)
        product_class = buildings('HVAC2_PDRSAug24_product_class', period)

        climate_zone = buildings('HVAC2_PDRSAug24_certificate_climate_zone', period)
        climate_zone_str = np.select([climate_zone == 1, climate_zone == 2, climate_zone == 3],
                                     ['hot_zone', 'average_zone', 'cold_zone'])
        # average

        in_hot_zone = (climate_zone_str == 'hot_zone')
        in_average_zone = (climate_zone_str == 'average_zone')
        in_cold_zone = (climate_zone_str == 'cold_zone')

        AC_HSPF = np.where(in_cold_zone, AC_HSPF_cold, AC_HSPF_mixed)
        # AC_HSPF_mixed
                
        # determines which HSPF value to use
        HSPF_is_zero = (
                        (AC_HSPF == 0) + 
                        (AC_HSPF == None)
                        )
        
        # tells you if the relevant HSPF is zero or non-existant
        AC_exceeds_benchmark = np.select([
                                            HSPF_is_zero,
                                            np.logical_not(HSPF_is_zero) * in_cold_zone,
                                            np.logical_not(HSPF_is_zero) * np.logical_not(in_cold_zone),
                                            ],
                                            [
            (AC_ACOP >= parameters(period).ESS.HEAB.table_F4_4_product_class['ACOP'][product_class]),
            (AC_HSPF >= parameters(period).ESS.HEAB.table_F4_4_product_class['HSPF_cold'][product_class]),
            (AC_HSPF >= parameters(period).ESS.HEAB.table_F4_4_product_class['HSPF_mixed'][product_class])
                                            ]
            )
        return AC_exceeds_benchmark