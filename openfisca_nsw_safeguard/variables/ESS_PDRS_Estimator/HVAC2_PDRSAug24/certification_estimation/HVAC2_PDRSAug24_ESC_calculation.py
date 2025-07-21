from email.mime import base
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

np.set_printoptions(suppress=True)


class HVAC2_PDRSAug24_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual heating energy use'
    metadata = {
        "alias": "Annual heating energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      heating_capacity = buildings('HVAC2_PDRSAug24_heating_capacity_input', period)
      equivalent_heating_hours = buildings('HVAC2_PDRSAug24_equivalent_heating_hours_input', period)
      rated_ACOP = buildings('HVAC2_PDRSAug24_rated_ACOP_input', period)
      
      return np.select([    
                            rated_ACOP == 0,
                            (heating_capacity * equivalent_heating_hours) > 0, 
                            (heating_capacity * equivalent_heating_hours) == 0,
                            (heating_capacity * equivalent_heating_hours) < 0
                        ],
                        [
                            0,
                            (heating_capacity * equivalent_heating_hours) / rated_ACOP,
                            0,
                            (heating_capacity * equivalent_heating_hours) / rated_ACOP
                        ])

class HVAC2_PDRSAug24_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual cooling energy use'
    metadata = {
        "alias": "Annual cooling energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      cooling_capacity = buildings('HVAC2_PDRSAug24_cooling_capacity_input', period)
      equivalent_cooling_hours = buildings('HVAC2_PDRSAug24_equivalent_cooling_hours_input', period)
      rated_AEER = buildings('HVAC2_PDRSAug24_rated_AEER_input', period)

      return np.select([    
                    rated_AEER == 0,
                    (cooling_capacity * equivalent_cooling_hours) > 0, 
                    (cooling_capacity * equivalent_cooling_hours) == 0,
                    (cooling_capacity * equivalent_cooling_hours) < 0
                ],
                [
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / rated_AEER, 
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / rated_AEER
                ])


class HVAC2_PDRSAug24_reference_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Reference annual heating energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      heating_capacity = buildings('HVAC2_PDRSAug24_heating_capacity_input', period)
      equivalent_heating_hours = buildings('HVAC2_PDRSAug24_equivalent_heating_hours_input', period)
      baseline_ACOP = buildings('HVAC2_PDRSAug24_baseline_ACOP_input', period)
      
      return np.select([    
                        baseline_ACOP == 0,
                        (heating_capacity * equivalent_heating_hours) > 0, 
                        (heating_capacity * equivalent_heating_hours) == 0,
                        (heating_capacity * equivalent_heating_hours) < 0
                    ],
                    [
                        0,
                        (heating_capacity * equivalent_heating_hours) / baseline_ACOP,
                        0,
                        (heating_capacity * equivalent_heating_hours) / baseline_ACOP
                    ])


class HVAC2_PDRSAug24_THEC_or_annual_heating(Variable):
    #Check if there is a THEC and if not, use the annual heating energy use formula
    value_type = float
    entity = Building
    definition_period = ETERNITY
   
    def formula(buildings, period, parameters):
        thec = buildings('HVAC2_PDRSAug24_commercial_THEC',period)
        refheat = buildings('HVAC2_PDRSAug24_heating_annual_energy_use',period)

        result_to_return = np.select([
                thec > 0, 
                thec <= 0 #if there is no THEC
            ],
            [
                thec,
                refheat
            ])
        return result_to_return
  

class HVAC2_PDRSAug24_reference_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Reference annual cooling energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      cooling_capacity = buildings('HVAC2_PDRSAug24_cooling_capacity_input', period)
      equivalent_cooling_hours = buildings('HVAC2_PDRSAug24_equivalent_cooling_hours_input', period)
      baseline_AEER = buildings('HVAC2_PDRSAug24_baseline_AEER_input', period)
      
      return np.select([  
                    baseline_AEER == 0,  
                    (cooling_capacity * equivalent_cooling_hours) > 0, 
                    (cooling_capacity * equivalent_cooling_hours) == 0,
                    (cooling_capacity * equivalent_cooling_hours) < 0
                ],
                [
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / baseline_AEER, 
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / baseline_AEER
                ])


class HVAC2_PDRSAug24_TCEC_or_annual_cooling(Variable):
    #Check if there is a TCEC and if not, use the annual cooling energy use formula
    value_type = float
    entity = Building
    definition_period = ETERNITY
   
    def formula(buildings, period, parameters):
        tcec = buildings('HVAC2_PDRSAug24_commercial_TCEC',period)
        refcool = buildings('HVAC2_PDRSAug24_cooling_annual_energy_use',period)

        result_to_return = np.select([
                tcec > 0, 
                tcec <= 0 #if there is no TCEC
            ],
            [
                tcec,
                refcool
            ])
        return result_to_return


class HVAC2_PDRSAug24_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "alias": "Deemed activity electricity savings",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      reference_annual_cooling = buildings('HVAC2_PDRSAug24_reference_cooling_annual_energy_use', period)
      annual_cooling = buildings('HVAC2_PDRSAug24_TCEC_or_annual_cooling', period)
      reference_annual_heating = buildings('HVAC2_PDRSAug24_reference_heating_annual_energy_use', period)
      annual_heating = buildings('HVAC2_PDRSAug24_THEC_or_annual_heating', period)
      lifetime = parameters(period).PDRS.AC.AC_related_constants.lifetime
      
      deemed_electricity_savings = np.multiply(((reference_annual_cooling - annual_cooling) + (reference_annual_heating - annual_heating)), (lifetime / 1000))
      return deemed_electricity_savings
    

class HVAC2_PDRSAug24_AC_Type(Enum):
    non_ducted_split_system = 'Non-ducted split system'
    ducted_split_system = 'Ducted split system'
    non_ducted_unitary_system = 'Non-ducted unitary system'
    ducted_unitary_system = 'Ducted unitary system'


class HVAC2_PDRSAug24_Air_Conditioner_type_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = HVAC2_PDRSAug24_AC_Type
    default_value = HVAC2_PDRSAug24_AC_Type.non_ducted_split_system
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


class HVAC2_PDRSAug24_Activity_savings(Variable):
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
    

class HVAC2_PDRSAug24_annual_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual ESS energy savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      #baseline AEER
      cooling_capacity = buildings('HVAC2_PDRSAug24_cooling_capacity_input', period)
      air_conditioner_type = buildings('HVAC2_PDRSAug24_Air_Conditioner_type', period)
      new_or_replacement_activity = buildings('HVAC2_PDRSAug24_Activity', period)

      cooling_capacity_to_check = np.select(
            [
                cooling_capacity < 4,
                (cooling_capacity < 10) * (cooling_capacity >= 4),
                (cooling_capacity < 39) * (cooling_capacity >= 10),
                (cooling_capacity < 65) * (cooling_capacity >= 39),
                cooling_capacity > 65
            ],
            [
                "less_than_4kW",
                "4kW_to_10kW",
                "10kW_to_39kW",
                "39kW_to_65kW",
                "more_than_65kW"
            ])
      
      aircon = np.select(
            [air_conditioner_type == HVAC2_PDRSAug24_AC_Type.non_ducted_split_system, 
             air_conditioner_type == HVAC2_PDRSAug24_AC_Type.ducted_split_system, air_conditioner_type == HVAC2_PDRSAug24_AC_Type.non_ducted_unitary_system, air_conditioner_type == HVAC2_PDRSAug24_AC_Type.ducted_unitary_system],
            
                ["non_ducted_split_system", "ducted_split_system", "non_ducted_unitary_system", "ducted_unitary_system"]
            )
        
      baseline_AEER = np.select(
            [new_or_replacement_activity == HVAC2_PDRSAug24_Activity_Type.new_installation_activity,
                new_or_replacement_activity == HVAC2_PDRSAug24_Activity_Type.replacement_activity],
            
                [parameters(period).ESS.HEAB.table_F4_2.AEER[aircon][cooling_capacity_to_check],
                    parameters(period).ESS.HEAB.table_F4_3.AEER[aircon][cooling_capacity_to_check]
                    ]
            )

      #equivalent cooling hours
      climate_zone = buildings('HVAC2_PDRSAug24_certificate_climate_zone', period)
      climate_zone_str = np.select([climate_zone == 1, climate_zone == 2, climate_zone == 3],
                                    ['hot_zone', 'average_zone', 'cold_zone'])
      equivalent_cooling_hours = parameters(period).ESS.HEAB.table_F4_1.equivalent_cooling_hours[climate_zone_str]

      #rated AEER
      rated_AEER = buildings('HVAC2_PDRSAug24_rated_AEER_input', period)

      #cooling annual energy use
      annual_cooling = np.select([  
                    rated_AEER == 0,
                    (cooling_capacity * equivalent_cooling_hours) > 0, 
                    (cooling_capacity * equivalent_cooling_hours) == 0,
                    (cooling_capacity * equivalent_cooling_hours) < 0
                ],
                [
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / rated_AEER, 
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / rated_AEER
                ])

      #TCEC or annual cooling
      tcec = buildings('HVAC2_PDRSAug24_commercial_TCEC',period)

      tcec_or_annual_cooling = np.select([
            tcec > 0, 
            tcec <= 0 #if there is no TCEC use annual cooling energy formula
        ],
        [
            tcec,
            annual_cooling
        ])

      #reference cooling energy use
      reference_cooling = np.select([  
                    baseline_AEER == 0,  
                    (cooling_capacity * equivalent_cooling_hours) > 0, 
                    (cooling_capacity * equivalent_cooling_hours) == 0,
                    (cooling_capacity * equivalent_cooling_hours) < 0
                ],
                [
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / baseline_AEER, 
                    0,
                    (cooling_capacity * equivalent_cooling_hours) / baseline_AEER
                ])

      #baseline ACOP
      cooling_capacity_to_check = np.select(
            [
                cooling_capacity < 4,
                (cooling_capacity < 10) * (cooling_capacity >= 4),
                (cooling_capacity < 39) * (cooling_capacity >= 10),
                (cooling_capacity < 65) * (cooling_capacity >= 39),
                cooling_capacity > 65
            ],
            [
                "less_than_4kW",
                "4kW_to_10kW",
                "10kW_to_39kW",
                "39kW_to_65kW",
                "more_than_65kW"
            ])
      
      aircon = np.select(
            [air_conditioner_type == HVAC2_PDRSAug24_AC_Type.non_ducted_split_system, air_conditioner_type == HVAC2_PDRSAug24_AC_Type.ducted_split_system, air_conditioner_type == HVAC2_PDRSAug24_AC_Type.non_ducted_unitary_system, air_conditioner_type == HVAC2_PDRSAug24_AC_Type.ducted_unitary_system],
            
                ["non_ducted_split_system", "ducted_split_system", "non_ducted_unitary_system", "ducted_unitary_system"]
            )
        
      baseline_ACOP = np.select(
            [new_or_replacement_activity == HVAC2_PDRSAug24_Activity_Type.new_installation_activity,
                new_or_replacement_activity == HVAC2_PDRSAug24_Activity_Type.replacement_activity],
            
                [parameters(period).ESS.HEAB.table_F4_2.ACOP[aircon][cooling_capacity_to_check],
                    parameters(period).ESS.HEAB.table_F4_3.ACOP[aircon][cooling_capacity_to_check]
                    ]
            )

      #heating capacity input
      heating_capacity = buildings('HVAC2_PDRSAug24_heating_capacity_input', period)

      #equivalent heating hours
      equivalent_heating_hours = parameters(period).ESS.HEAB.table_F4_1.equivalent_heating_hours[climate_zone_str]

      #rated ACOP
      rated_ACOP = buildings('HVAC2_PDRSAug24_rated_ACOP_input', period)
      
      aircon = np.select(
            [air_conditioner_type == HVAC2_PDRSAug24_AC_Type.non_ducted_split_system, air_conditioner_type == HVAC2_PDRSAug24_AC_Type.ducted_split_system, air_conditioner_type == HVAC2_PDRSAug24_AC_Type.non_ducted_unitary_system, air_conditioner_type == HVAC2_PDRSAug24_AC_Type.ducted_unitary_system],
            
                ["non_ducted_split_system", "ducted_split_system", "non_ducted_unitary_system", "ducted_unitary_system"]
            )
        
      baseline_ACOP = np.select(
            [new_or_replacement_activity == HVAC2_PDRSAug24_Activity_Type.new_installation_activity,
                new_or_replacement_activity == HVAC2_PDRSAug24_Activity_Type.replacement_activity],
            
                [parameters(period).ESS.HEAB.table_F4_2.ACOP[aircon][cooling_capacity_to_check],
                    parameters(period).ESS.HEAB.table_F4_3.ACOP[aircon][cooling_capacity_to_check]
                    ]
            )

      #heating annual energy use
      annual_heating = np.select([  
                    rated_ACOP == 0,
                    (heating_capacity * equivalent_heating_hours) > 0, 
                    (heating_capacity * equivalent_heating_hours) == 0,
                    (heating_capacity * equivalent_heating_hours) < 0
                ],
                [
                    0,
                    (heating_capacity * equivalent_heating_hours) / rated_ACOP, 
                    0,
                    (heating_capacity * equivalent_heating_hours) / rated_ACOP
                ])

      #THEC or annual heating
      thec = buildings('HVAC2_PDRSAug24_commercial_THEC',period)

      thec_or_annual_heating = np.select([
                thec > 0, 
                thec <= 0 #if there is no THEC
            ],
            [
                thec,
                annual_heating
            ])

      #reference heating annual energy use
      reference_heating = np.select([    
                            baseline_ACOP == 0,
                            (heating_capacity * equivalent_heating_hours) > 0, 
                            (heating_capacity * equivalent_heating_hours) == 0,
                            (heating_capacity * equivalent_heating_hours) < 0
                        ],
                        [
                            0,
                            (heating_capacity * equivalent_heating_hours) / baseline_ACOP,
                            0,
                            (heating_capacity * equivalent_heating_hours) / baseline_ACOP
                        ])
      
      #deemed electricity savings
      lifetime = parameters(period).PDRS.AC.AC_related_constants.lifetime
      deemed_electricity_savings = np.multiply(((reference_cooling - tcec_or_annual_cooling) + (reference_heating - thec_or_annual_heating)), (lifetime / 1000))
      
      #regional network factor
      postcode = buildings('HVAC2_PDRSAug24_PDRS__postcode', period)
      rnf = parameters(period).PDRS.table_A24_regional_network_factor
      regional_network_factor = rnf.calc(postcode)

      #electricity savings
      annual_savings = (deemed_electricity_savings * regional_network_factor)
      annual_savings_return = np.select([
            annual_savings <= 0, annual_savings > 0
        ],
	    [
            0, annual_savings
        ])
      return annual_savings_return
      

class HVAC2_PDRSAug24_PDRS__regional_network_factor(Variable):
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
        postcode = buildings('HVAC2_PDRSAug24_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided


class HVAC2_PDRSAug24_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HVAC2 Electricity savings'
    metadata = {
        "alias": "HVAC2 electricity savings",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('HVAC2_PDRSAug24_deemed_activity_electricity_savings', period)  # 2798.25 
        regional_network_factor = buildings('HVAC2_PDRSAug24_PDRS__regional_network_factor', period)

        electricity_savings = (deemed_electricity_savings * regional_network_factor)
        return electricity_savings


class HVAC2_PDRSAug24_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for HVAC2'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      HVAC2_electricity_savings = buildings('HVAC2_PDRSAug24_electricity_savings', period)
      HVAC2_TCSPF_or_AEER_exceeds_ESS_benchmark = buildings('HVAC2_PDRSAug24_TCSPF_or_AEER_exceeds_ESS_benchmark', period)
      HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark = buildings('HVAC2_PDRSAug24_HSPF_or_ACOP_exceeds_ESS_benchmark', period)
      electricity_certificate_conversion_factor = 1.06
      heating_capacity = buildings('HVAC2_PDRSAug24_heating_capacity_input', period) 
      zero_heating_capacity = ( heating_capacity == 0 )
      
      result = np.floor(HVAC2_electricity_savings * electricity_certificate_conversion_factor)
      result_meet_elig = np.select([
                         np.logical_not(zero_heating_capacity) * HVAC2_TCSPF_or_AEER_exceeds_ESS_benchmark * HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark, 
                         np.logical_not(zero_heating_capacity) * np.logical_not(HVAC2_TCSPF_or_AEER_exceeds_ESS_benchmark) * HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark,
                         np.logical_not(zero_heating_capacity) * HVAC2_TCSPF_or_AEER_exceeds_ESS_benchmark * np.logical_not(HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         np.logical_not(zero_heating_capacity) * np.logical_not(HVAC2_TCSPF_or_AEER_exceeds_ESS_benchmark) * np.logical_not(HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         zero_heating_capacity * HVAC2_TCSPF_or_AEER_exceeds_ESS_benchmark * np.logical_not(HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         zero_heating_capacity * np.logical_not(HVAC2_TCSPF_or_AEER_exceeds_ESS_benchmark) * np.logical_not(HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         zero_heating_capacity * HVAC2_TCSPF_or_AEER_exceeds_ESS_benchmark * HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark
                         ],
                        [
                            result, 0, 0, 0, 0, 0, 0
                        ],
                        result
      )
      
      result_to_return = np.select([
                result_meet_elig <= 0, result_meet_elig > 0
            ], [
                0, result_meet_elig
            ])

      return result_to_return