from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import math

import numpy as np


class HVAC2_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual heating energy use'
    metadata = {
        "alias": "Annual heating energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      heating_capacity = buildings('HVAC2_heating_capacity_input', period)
      equivalent_heating_hours = buildings('HVAC2_equivalent_heating_hours_input', period)
      rated_ACOP = buildings('HVAC2_rated_ACOP_input', period)
      
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


class HVAC2_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual cooling energy use'
    metadata = {
        "alias": "Annual cooling energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      cooling_capacity = buildings('HVAC2_cooling_capacity_input', period)
      equivalent_cooling_hours = buildings('HVAC2_equivalent_cooling_hours_input', period)
      rated_AEER = buildings('HVAC2_rated_AEER_input', period)

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


class HVAC2_reference_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Reference annual heating energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      heating_capacity = buildings('HVAC2_heating_capacity_input', period)
      equivalent_heating_hours = buildings('HVAC2_equivalent_heating_hours_input', period)
      baseline_ACOP = buildings('HVAC2_baseline_ACOP_input', period)

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

class HVAC2_THEC_or_annual_heating(Variable):
    #Check if there is a THEC and if not, use the annual heating energy use formula
    value_type = float
    entity = Building
    definition_period = ETERNITY
   
    def formula(buildings, period, parameters):
        thec = buildings('HVAC2_commercial_THEC',period)
        refheat = buildings('HVAC2_heating_annual_energy_use',period)

        result_to_return = np.select([
                thec > 0, 
                thec <= 0 #if there is no THEC
            ],
            [
                thec,
                refheat
            ])
        return result_to_return


class HVAC2_reference_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Reference annual cooling energy use",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      cooling_capacity = buildings('HVAC2_cooling_capacity_input', period)
      equivalent_cooling_hours = buildings('HVAC2_equivalent_cooling_hours_input', period)
      baseline_AEER = buildings('HVAC2_baseline_AEER_input', period)
      
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


class HVAC2_TCEC_or_annual_cooling(Variable):
    #Check if there is a TCEC and if not, use the annual cooling energy use formula
    value_type = float
    entity = Building
    definition_period = ETERNITY
   
    def formula(buildings, period, parameters):
        tcec = buildings('HVAC2_commercial_TCEC',period)
        refcool = buildings('HVAC2_cooling_annual_energy_use',period)

        result_to_return = np.select([
                tcec > 0, 
                tcec <= 0 #if there is no TCEC
            ],
            [
                tcec,
                refcool
            ])
        return result_to_return


class HVAC2_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "alias": "Deemed activity electricity savings",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      reference_annual_cooling = buildings('HVAC2_reference_cooling_annual_energy_use', period)
      annual_cooling = buildings('HVAC2_TCEC_or_annual_cooling', period)
      reference_annual_heating = buildings('HVAC2_reference_heating_annual_energy_use', period)
      annual_heating = buildings('HVAC2_THEC_or_annual_heating', period)
      lifetime = 10
      
      deemed_electricity_savings = np.multiply(((reference_annual_cooling - annual_cooling) + (reference_annual_heating - annual_heating)), (lifetime / 1000))
      return deemed_electricity_savings
    

class HVAC2_AC_Type(Enum):
    non_ducted_split_system = 'Non-ducted split system'
    ducted_split_system = 'Ducted split system'
    non_ducted_unitary_system = 'Non-ducted unitary system'
    ducted_unitary_system = 'Ducted unitary system'


class HVAC2_Air_Conditioner_type_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = HVAC2_AC_Type
    default_value = HVAC2_AC_Type.non_ducted_split_system
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label': 'Air conditioner type',
        'display_question' : 'What is your air conditioner type?',
        'sorting' : 4
    }


class HVAC2_Activity_Type(Enum):
    new_installation_activity = 'Installation of a new air conditioner'
    replacement_activity = 'Replacement of an existing air conditioner'


class HVAC2_Activity_savings(Variable):
    value_type = Enum
    entity = Building
    possible_values = HVAC2_Activity_Type
    default_value = HVAC2_Activity_Type.replacement_activity
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label': 'Replacement or new installation activity',
        'display_question' : 'Which one of the following activities are you implementing?',
        'sorting' : 3
    }


class HVAC2_annual_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual ESS energy savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      #baseline AEER
      cooling_capacity = buildings('HVAC2_cooling_capacity_input', period)
      air_conditioner_type = buildings('HVAC2_Air_Conditioner_type', period)
      new_or_replacement_activity = buildings('HVAC2_Activity', period)

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
            [   air_conditioner_type == HVAC2_AC_Type.non_ducted_split_system, 
                air_conditioner_type == HVAC2_AC_Type.ducted_split_system, 
                air_conditioner_type == HVAC2_AC_Type.non_ducted_unitary_system, 
                air_conditioner_type == HVAC2_AC_Type.ducted_unitary_system
            ],
            [   'non_ducted_split_system', 
                'ducted_split_system', 
                'non_ducted_unitary_system', 
                'ducted_unitary_system'
            ])

      baseline_AEER = np.select(
            [new_or_replacement_activity == HVAC2_Activity_Type.new_installation_activity,
                new_or_replacement_activity == HVAC2_Activity_Type.replacement_activity
            ],
            [parameters(period).ESS.HEAB.table_F4_2.AEER[aircon][cooling_capacity_to_check], 
                    parameters(period).ESS.HEAB.table_F4_3.AEER[aircon][cooling_capacity_to_check] 
            ])

      #equivalent cooling hours
      climate_zone = buildings('HVAC2_certificate_climate_zone', period)
      climate_zone_str = np.select([climate_zone == 1, climate_zone == 2, climate_zone == 3],
                                    ['hot_zone', 'average_zone', 'cold_zone'])
      
      in_hot_zone = (climate_zone_str == 'hot_zone')
      in_average_zone = (climate_zone_str == 'average_zone')
      in_cold_zone = (climate_zone_str == 'cold_zone')
      equivalent_cooling_hours = parameters(period).ESS.HEAB.table_F4_1.equivalent_cooling_hours[climate_zone_str]

      #rated AEER
      rated_AEER = buildings('HVAC2_rated_AEER_input', period)

      #TCSPF
      AC_TCSPF = buildings('HVAC2_TCSPF_mixed', period)
      cooling_capacity_TCSPF = np.select(
                                    [
                                        (cooling_capacity < 4),
                                        ((cooling_capacity >= 4) * (cooling_capacity < 6)),
                                        ((cooling_capacity >= 6) * (cooling_capacity < 10)),
                                        ((cooling_capacity >= 10) * (cooling_capacity < 13)),
                                        ((cooling_capacity >= 13) * (cooling_capacity < 25)),
                                        ((cooling_capacity >= 25) * (cooling_capacity <= 65)),
                                        (cooling_capacity > 65)
                                    ],
                                    [
                                        "less_than_4kW",
                                        "4kW_to_6kW",
                                        "6kW_to_10kW",
                                        "10kW_to_13kW",
                                        "13kW_to_25kW",
                                        "25kW_to_65kW",
                                        "over_65kW"
                                    ])
      
      #check if TCSPF or AEER exceeds benchmark
      TCSPF_is_zero = ((AC_TCSPF == 0) + (AC_TCSPF == None))
      AC_exceeds_TCSPF_AEER_benchmark = np.where(
            TCSPF_is_zero,
            (rated_AEER >= parameters(period).PDRS.AC.table_HVAC_2_4[air_conditioner_type][cooling_capacity_TCSPF]),
            (AC_TCSPF >= parameters(period).PDRS.AC.table_HVAC_2_3[air_conditioner_type][cooling_capacity_TCSPF])
        )
  
      #cooling annual energy use (this is only used if there is no TCEC)
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
      tcec = buildings('HVAC2_commercial_TCEC',period)
   
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
      
      baseline_ACOP = np.select(
            [new_or_replacement_activity == HVAC2_Activity_Type.new_installation_activity,
                new_or_replacement_activity == HVAC2_Activity_Type.replacement_activity
            ],
            [parameters(period).ESS.HEAB.table_F4_2.ACOP[aircon][cooling_capacity_to_check],
                    parameters(period).ESS.HEAB.table_F4_3.ACOP[aircon][cooling_capacity_to_check]
            ])

      #heating capacity input
      heating_capacity = buildings('HVAC2_heating_capacity_input', period)

      #equivalent heating hours
      equivalent_heating_hours = parameters(period).ESS.HEAB.table_F4_1.equivalent_heating_hours[climate_zone_str]
  
      #rated ACOP
      rated_ACOP = buildings('HVAC2_rated_ACOP_input', period)

      #HSPF
      AC_HSPF_mixed = buildings('HVAC2_HSPF_mixed', period)
      AC_HSPF_cold = buildings('HVAC2_HSPF_cold', period)
      cooling_capacity_HSPF = np.select(
                                    [
                                        (cooling_capacity < 4),
                                        ((cooling_capacity >= 4) * (cooling_capacity < 6)),
                                        ((cooling_capacity >= 6) * (cooling_capacity < 10)),
                                        ((cooling_capacity >= 10) * (cooling_capacity < 13)),
                                        ((cooling_capacity >= 13) * (cooling_capacity < 25)),
                                        ((cooling_capacity >= 25) * (cooling_capacity <= 65)),
                                        (cooling_capacity > 65)
                                    ],
                                    [
                                        "less_than_4kW",
                                        "4kW_to_6kW",
                                        "6kW_to_10kW",
                                        "10kW_to_13kW",
                                        "13kW_to_25kW",
                                        "25kW_to_65kW",
                                        "over_65kW"
                                    ])
      #tells you if the relevant HSPF is zero or non-existent
    #   HSPF_is_zero = ((AC_HSPF_mixed == 0) + (AC_HSPF_mixed == None) + (AC_HSPF_cold == 0) + (AC_HSPF_cold == None))
    #   HSPF_to_use = np.where(
    #             HSPF_is_zero,
    #             np.logical_not(HSPF_is_zero) * in_cold_zone,
    #             np.logical_not(HSPF_is_zero) * np.logical_not(in_cold_zone),
    #         )

    #   AC_exceeds_HSPF_ACOP_benchmark = np.select(
    #         [
    #             HSPF_is_zero,
    #             np.logical_not(HSPF_is_zero) * in_cold_zone,
    #             np.logical_not(HSPF_is_zero) * np.logical_not(in_cold_zone),
    #         ],
    #         [
    #             (rated_ACOP >= parameters(period).ESS.HEAB.table_F4_5['ACOP'][air_conditioner_type][cooling_capacity_HSPF]),
    #             (AC_HSPF >= parameters(period).ESS.HEAB.table_F4_4['HSPF_cold'][air_conditioner_type][cooling_capacity_HSPF]),
    #             (AC_HSPF >= parameters(period).ESS.HEAB.table_F4_4['HSPF_mixed'][air_conditioner_type][cooling_capacity_HSPF])
    #         ])
     
      #check if HSPF or ACOP exceeds benchmark
    #   AC_exceeds_HSPF_ACOP_benchmark = np.where(
    #          (rated_ACOP >= parameters(period).ESS.HEAB.table_F4_5['ACOP'][air_conditioner_type][cooling_capacity_HSPF]),
    #          (HSPF_to_use >= parameters(period).ESS.HEAB.table_F4_4['HSPF_cold'][air_conditioner_type][cooling_capacity_HSPF]),
    #          (HSPF_to_use >= parameters(period).ESS.HEAB.table_F4_4['HSPF_mixed'][air_conditioner_type][cooling_capacity_HSPF])
    #   )

      AC_HSPF = np.where(
                        in_cold_zone,
                        AC_HSPF_cold,
                        AC_HSPF_mixed)
      # determines which HSPF value to use
      HSPF_is_zero = (
                    (AC_HSPF == 0) + 
                    (AC_HSPF == None)
                    )
      # tells you if the relevant HSPF is zero or non-existant
      AC_exceeds_HSPF_ACOP_benchmark = np.select([
                                        HSPF_is_zero,
                                        np.logical_not(HSPF_is_zero) * in_cold_zone,
                                        np.logical_not(HSPF_is_zero) * np.logical_not(in_cold_zone),
                                        ],
                                        [
      (rated_ACOP >= parameters(period).ESS.HEAB.table_F4_5['ACOP'][air_conditioner_type][cooling_capacity_HSPF]),
      (AC_HSPF >= parameters(period).ESS.HEAB.table_F4_4['HSPF_cold'][air_conditioner_type][cooling_capacity_HSPF]),
      (AC_HSPF >= parameters(period).ESS.HEAB.table_F4_4['HSPF_mixed'][air_conditioner_type][cooling_capacity_HSPF])
                                        ]
        )

      baseline_ACOP = np.select(
            [new_or_replacement_activity == HVAC2_Activity_Type.new_installation_activity,
                new_or_replacement_activity == HVAC2_Activity_Type.replacement_activity],
                [parameters(period).ESS.HEAB.table_F4_2.ACOP[aircon][cooling_capacity_to_check],
                    parameters(period).ESS.HEAB.table_F4_3.ACOP[aircon][cooling_capacity_to_check]
                    ])
      
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
                    (cooling_capacity * equivalent_heating_hours) / rated_ACOP
                ])

      #THEC or annual heating
      thec = buildings('HVAC2_commercial_THEC',period)

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
      lifetime = 10

      #deemed electricity savings
      deemed_electricity_savings = np.multiply(((reference_cooling - tcec_or_annual_cooling) + (reference_heating - thec_or_annual_heating)), (lifetime / 1000))
  
      #regional network factor
      postcode = buildings('HVAC2_PDRS__postcode', period)
      rnf = parameters(period).PDRS.table_A24_regional_network_factor
      regional_network_factor = rnf.calc(postcode)

      #electricity savings
      annual_energy_savings = (deemed_electricity_savings * regional_network_factor)
      print('annual_energy_savings', annual_energy_savings)
      annual_savings_return = np.select([
            (annual_energy_savings <= 0 * AC_exceeds_HSPF_ACOP_benchmark * AC_exceeds_TCSPF_AEER_benchmark),
            (annual_energy_savings <= 0 * np.logical_not(AC_exceeds_HSPF_ACOP_benchmark) * AC_exceeds_TCSPF_AEER_benchmark),
            (annual_energy_savings <= 0 * np.logical_not(AC_exceeds_HSPF_ACOP_benchmark) * np.logical_not(AC_exceeds_TCSPF_AEER_benchmark)),
            (annual_energy_savings <= 0 * AC_exceeds_HSPF_ACOP_benchmark * np.logical_not(AC_exceeds_TCSPF_AEER_benchmark)),
            (annual_energy_savings > 0 * AC_exceeds_HSPF_ACOP_benchmark * AC_exceeds_TCSPF_AEER_benchmark),
            (annual_energy_savings > 0 * np.logical_not(AC_exceeds_HSPF_ACOP_benchmark) * AC_exceeds_TCSPF_AEER_benchmark),
            (annual_energy_savings > 0 * np.logical_not(AC_exceeds_HSPF_ACOP_benchmark) * np.logical_not(AC_exceeds_TCSPF_AEER_benchmark)),
            (annual_energy_savings > 0 * AC_exceeds_HSPF_ACOP_benchmark * np.logical_not(AC_exceeds_TCSPF_AEER_benchmark))
        ],
	    [
            0,
            0,
            0,
            0,
            annual_energy_savings,
            0,
            0,
            0
        ])
      print('AC_HSPF_mixed', AC_HSPF_mixed)
      print('AC_HSPF_cold', AC_HSPF_cold)
      print('HSPF_is_zero', HSPF_is_zero)
      print('AC_exceeds_HSPF_ACOP_benchmark', AC_exceeds_HSPF_ACOP_benchmark)
      print('AC_exceeds_TCSPF_AEER_benchmark', AC_exceeds_TCSPF_AEER_benchmark)
      print('annual_savings_return', annual_savings_return)
      return annual_savings_return


class HVAC2_PDRS__regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'
    metadata = {
        'variable-type': 'inter-interesting',
        'display_question': 'PDRS regional network factor'
        }

    def formula(buildings, period, parameters):
        postcode = buildings('HVAC2_PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided


class HVAC2_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HVAC2 Electricity savings'
    metadata = {
        "alias": "HVAC2 electricity savings",
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('HVAC2_deemed_activity_electricity_savings', period)   
        regional_network_factor = buildings('HVAC2_PDRS__regional_network_factor', period)

        electricity_savings = (deemed_electricity_savings * regional_network_factor)
        return electricity_savings


class HVAC2_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for HVAC2'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      electricity_savings = buildings('HVAC2_electricity_savings', period)
      HVAC2_TCSPF_or_AEER_exceeds_benchmark = buildings('HVAC2_TCSPF_or_AEER_exceeds_benchmark', period)
      HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark = buildings('HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark', period)
      electricity_certificate_conversion_factor = 1.06
      heating_capacity = buildings('HVAC2_heating_capacity_input', period)
      zero_heating_capacity = ( heating_capacity == 0)

      result = np.floor(electricity_savings * electricity_certificate_conversion_factor)      
      result_meet_elig = np.select([
                         np.logical_not(zero_heating_capacity) * HVAC2_TCSPF_or_AEER_exceeds_benchmark * HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark, 
                         np.logical_not(zero_heating_capacity) * np.logical_not(HVAC2_TCSPF_or_AEER_exceeds_benchmark) * HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark,
                         np.logical_not(zero_heating_capacity) * HVAC2_TCSPF_or_AEER_exceeds_benchmark * np.logical_not(HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         np.logical_not(zero_heating_capacity) * np.logical_not(HVAC2_TCSPF_or_AEER_exceeds_benchmark) * np.logical_not(HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         zero_heating_capacity * HVAC2_TCSPF_or_AEER_exceeds_benchmark * np.logical_not(HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         zero_heating_capacity * np.logical_not(HVAC2_TCSPF_or_AEER_exceeds_benchmark) * np.logical_not(HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark),
                         zero_heating_capacity * HVAC2_TCSPF_or_AEER_exceeds_benchmark * HVAC2_HSPF_or_ACOP_exceeds_ESS_benchmark
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
