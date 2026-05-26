from email.mime import base
from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building

import numpy as np

np.set_printoptions(suppress=True)


class HVAC1_PDRSAug24_heating_annual_energy_use(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual heating energy use'
    metadata = {
        "alias": "Annual heating energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        heating_capacity = buildings('HVAC1_PDRSAug24_heating_capacity_input', period)
        equivalent_heating_hours = buildings('HVAC1_PDRSAug24_equivalent_heating_hours_input', period)
        rated_ACOP = buildings('HVAC1_PDRSAug24_rated_ACOP_input', period)
        numerator = heating_capacity * equivalent_heating_hours

        return np.divide(
            numerator,
            rated_ACOP,
            out=np.zeros_like(rated_ACOP, dtype=float),
            where=rated_ACOP != 0
        )


class HVAC1_PDRSAug24_cooling_annual_energy_use(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual cooling energy use'
    metadata = {
        "alias": "Annual cooling energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('HVAC1_PDRSAug24_cooling_capacity_input', period)
        equivalent_cooling_hours = buildings('HVAC1_PDRSAug24_equivalent_cooling_hours_input', period)
        rated_AEER = buildings('HVAC1_PDRSAug24_rated_AEER_input', period)
        numerator = cooling_capacity * equivalent_cooling_hours

        return np.divide(
            numerator,
            rated_AEER,
            out=np.zeros_like(rated_AEER, dtype=float),
            where=rated_AEER != 0
        )


class HVAC1_PDRSAug24_reference_heating_annual_energy_use(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Reference annual heating energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        heating_capacity = buildings('HVAC1_PDRSAug24_heating_capacity_input', period)
        equivalent_heating_hours = buildings('HVAC1_PDRSAug24_equivalent_heating_hours_input', period)
        baseline_ACOP = buildings('HVAC1_PDRSAug24_baseline_ACOP_input', period)
        numerator = heating_capacity * equivalent_heating_hours

        return np.divide(
            numerator,
            baseline_ACOP,
            out=np.zeros_like(baseline_ACOP, dtype=float),
            where=baseline_ACOP != 0
        )



class HVAC1_PDRSAug24_THEC_or_annual_heating(BaseVariable):
    #Check if there is a THEC and if not, use the annual heating energy use formula
    value_type = float
    entity = Building
    definition_period = ETERNITY
   
    def formula(buildings, period, parameters):
        thec = buildings('HVAC1_PDRSAug24_residential_THEC',period)
        refheat = buildings('HVAC1_PDRSAug24_heating_annual_energy_use',period)

        result_to_return = np.select([
                thec > 0, 
                thec <= 0 #if there is no THEC
            ],
            [
                thec,
                refheat
            ])
        return result_to_return
  

class HVAC1_PDRSAug24_reference_cooling_annual_energy_use(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Reference annual cooling energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('HVAC1_PDRSAug24_cooling_capacity_input', period)
        equivalent_cooling_hours = buildings('HVAC1_PDRSAug24_equivalent_cooling_hours_input', period)
        baseline_AEER = buildings('HVAC1_PDRSAug24_baseline_AEER_input', period)
        numerator = cooling_capacity * equivalent_cooling_hours

        return np.divide(
            numerator,
            baseline_AEER,
            out=np.zeros_like(baseline_AEER, dtype=float),
            where=baseline_AEER != 0
        )


class HVAC1_PDRSAug24_TCEC_or_annual_cooling(BaseVariable):
    #Check if there is a TCEC and if not, use the annual cooling energy use formula
    value_type = float
    entity = Building
    definition_period = ETERNITY
   
    def formula(buildings, period, parameters):
        tcec = buildings('HVAC1_PDRSAug24_residential_TCEC',period)
        refcool = buildings('HVAC1_PDRSAug24_cooling_annual_energy_use',period)

        result_to_return = np.select([
                tcec > 0, 
                tcec <= 0 #if there is no TCEC
            ],
            [
                tcec,
                refcool
            ])
        return result_to_return


class HVAC1_PDRSAug24_deemed_activity_electricity_savings(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "alias": "Deemed activity electricity savings",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      reference_annual_cooling = buildings('HVAC1_PDRSAug24_reference_cooling_annual_energy_use', period)
      annual_cooling = buildings('HVAC1_PDRSAug24_TCEC_or_annual_cooling', period)
      reference_annual_heating = buildings('HVAC1_PDRSAug24_reference_heating_annual_energy_use', period)
      annual_heating = buildings('HVAC1_PDRSAug24_THEC_or_annual_heating', period)
      lifetime = parameters(period).ESS.ESS_D16.related_constants.lifetime
      
      deemed_electricity_savings = np.multiply(((reference_annual_cooling - annual_cooling) + (reference_annual_heating - annual_heating)), (lifetime / 1000))
      return deemed_electricity_savings
    

class HVAC1_PDRSAug24_AC_Type(Enum):
    non_ducted_single_split_system = 'Non-ducted single split system'
    ducted_single_split_system = 'Ducted single split system'
    non_ducted_multi_split_system = 'Non-ducted multi-split system'
    ducted_multi_split_system = 'Ducted multi-split system'
    non_ducted_unitary_system = 'Non-ducted unitary system'
    ducted_unitary_system = 'Ducted unitary system'


class HVAC1_PDRSAug24_Air_Conditioner_type_savings(BaseVariable):
    value_type = Enum
    entity = Building
    possible_values = HVAC1_PDRSAug24_AC_Type
    default_value = HVAC1_PDRSAug24_AC_Type.non_ducted_single_split_system
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label': 'Air conditioner type',
        'display_question' : 'What is your air conditioner type?',
        'sorting' : 4
    }


class HVAC1_PDRSAug24_Activity_Type(Enum):
    new_installation_activity = 'Installation of a new air conditioner'
    replacement_activity = 'Replacement of an existing air conditioner'


class HVAC1_PDRSAug24_Activity_savings(BaseVariable):
    value_type = Enum
    entity = Building
    possible_values = HVAC1_PDRSAug24_Activity_Type
    default_value = HVAC1_PDRSAug24_Activity_Type.replacement_activity
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label': 'Replacement or new installation activity',
        'display_question' : 'Which one of the following activities are you implementing?',
        'sorting' : 3
    }
    

class HVAC1_PDRSAug24_annual_energy_savings(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual ESS energy savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        # annual_savings = deemed_electricity_savings
        deemed_electricity_savings = buildings('HVAC1_PDRSAug24_deemed_activity_electricity_savings', period)  # 2798.25 
        annual_savings = (deemed_electricity_savings)
        annual_savings_return = np.select([
                annual_savings <= 0, annual_savings > 0
            ],
            [
                0, annual_savings
            ])

        return annual_savings_return
      

class HVAC1_PDRSAug24_PDRS__regional_network_factor(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'
    metadata = {
        "variable-type" : "inter-interesting",
        "alias" :"PDRS Regional Network Factor",
        "display_question" : "PDRS regional network factor"
    }

    def formula(buildings, period, parameters):
        postcode = buildings('HVAC1_PDRSAug24_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided


class HVAC1_PDRSAug24_electricity_savings(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HVAC1 Electricity savings'
    metadata = {
        "alias": "HVAC1 electricity savings",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('HVAC1_PDRSAug24_deemed_activity_electricity_savings', period)  # 2798.25 
        electricity_savings = (deemed_electricity_savings)
        return electricity_savings


class HVAC1_PDRSAug24_ESC_calculation(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for HVAC1'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      HVAC1_electricity_savings = buildings('HVAC1_PDRSAug24_electricity_savings', period)
      regional_network_factor = buildings('HVAC1_PDRSAug24_PDRS__regional_network_factor', period)
      HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark = buildings('HVAC1_PDRSAug24_TCSPF_or_AEER_exceeds_ESS_benchmark', period)
      HVAC1_HSPF_or_ACOP_exceeds_ESS_benchmark = buildings('HVAC1_PDRSAug24_HSPF_or_ACOP_exceeds_ESS_benchmark', period)
      electricity_certificate_conversion_factor = 1.06
      heating_capacity = buildings('HVAC1_PDRSAug24_heating_capacity_input', period) 
      zero_heating_capacity = ( heating_capacity == 0)
      
      result = np.floor(HVAC1_electricity_savings * regional_network_factor * electricity_certificate_conversion_factor)
      result_meet_elig = np.select([
                         np.logical_not(zero_heating_capacity) * HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark * HVAC1_HSPF_or_ACOP_exceeds_ESS_benchmark, 
                         np.logical_not(zero_heating_capacity) * np.logical_not(HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark) * HVAC1_HSPF_or_ACOP_exceeds_ESS_benchmark,
                         np.logical_not(zero_heating_capacity) * HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark * np.logical_not(HVAC1_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         np.logical_not(zero_heating_capacity) * np.logical_not(HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark) * np.logical_not(HVAC1_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         zero_heating_capacity * HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark * np.logical_not(HVAC1_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         zero_heating_capacity * np.logical_not(HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark) * np.logical_not(HVAC1_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         zero_heating_capacity * HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark * HVAC1_HSPF_or_ACOP_exceeds_ESS_benchmark
                         ],
                        [
                            result, 0, 0, 0, 0, 0, 0
                        ],
                        result) 
      
      
      result_to_return = np.select([
                result_meet_elig <= 0, result_meet_elig > 0
            ], [
                0, result_meet_elig
            ])
      # Add cap value for ESC
      product_class_is_18_to_21 = buildings('HVAC1_PDRSAug24_product_class_is_18_to_21', period)
      climate_zone = buildings('HVAC1_PDRSAug24_certificate_climate_zone', period)

      # Cap value based on climate zone (only applied when product class is 18-21)
      # zone_int: 1 = hot, 2 = mixed/average, 3 = cold
      cap_value = np.select(
          [
              climate_zone == 3,                          # cold zone → cap 90
              (climate_zone == 1) | (climate_zone == 2),  # hot or mixed/average → cap 70
          ],
          [90, 70],
          default=70  # fallback
      )

      result_to_return = np.where(
          product_class_is_18_to_21,
          np.minimum(result_to_return, cap_value),  # apply zone-based cap
          result_to_return                          # unchanged
      )
      return result_to_return