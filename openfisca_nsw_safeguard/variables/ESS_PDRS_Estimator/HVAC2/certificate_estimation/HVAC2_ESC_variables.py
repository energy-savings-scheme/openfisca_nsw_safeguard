import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for HVAC2 ESC Calculation
    These variables use GEMS Registry data
"""
class HVAC2_heating_capacity_input(Variable):
    reference = 'unit in '
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Air Conditioner Heating Capacity",
        "display_question": "What is the heating capacity of your commercial air conditioner?"
    }

class HVAC2_cooling_capacity_input(Variable):
    reference = 'unit in kw'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Air Conditioner Cooling Capacity",
        'display_question': 'Rated cooling capacity at 35c as recorded in the GEMS Registry'
    }


class HVAC2_rated_ACOP_input(Variable):
    reference = 'unit in '
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Rated ACOP",
        "display_question": "What is the Rated ACOP of your commercial air conditioner?"
    }


class HVAC2_baseline_AEER_input(Variable):
    value_type = float
    entity = Building
    label = "Baseline AEER"
    definition_period = ETERNITY
    metadata = {
        "alias": "AEER",
        "variable-type": "output"
    }

    def formula(building, period, parameters):
        cooling_capacity = building(
            'HVAC2_cooling_capacity_input', period)
        
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
        
        air_conditioner_type = building('HVAC2_Air_Conditioner_type', period)
        aircon = np.select(
            [air_conditioner_type == HVAC2_AC_Type.non_ducted_split_system, air_conditioner_type == HVAC2_AC_Type.ducted_split_system, air_conditioner_type == HVAC2_AC_Type.non_ducted_unitary_system, air_conditioner_type == HVAC2_AC_Type.ducted_unitary_system],
            
                ["non_ducted_split_system", "ducted_split_system", "non_ducted_unitary_system", "ducted_unitary_system"]
            )
       
        new_or_used_equipment = building('HVAC2_New_Equipment', period)
        
        
        baseline_aeer = np.select(
            [new_or_used_equipment, np.logical_not(new_or_used_equipment)],
            
                [parameters(period).ESS.HEAB.table_F4_2.AEER[aircon][cooling_capacity_to_check], 
                    parameters(period).ESS.HEAB.table_F4_3.AEER[aircon][cooling_capacity_to_check] 
                    ]
            )

        return baseline_aeer


class HVAC2_rated_AEER_input(Variable):
    reference = 'unit in '
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Rated AEER",
        "display_question": "What is the Rated AEER of your commercial air conditioner?"
    }
    
class DefaultValuesCertificateClimateZone(Enum):
    hot_zone = "AC is installed in the hot zone."
    average_zone = "AC is installed in the average zone."
    cold_zone = "AC is installed in the cold zone."


class HVAC2_certificate_climate_zone(Variable):
    value_type = Enum
    entity = Building
    label = "Which climate zone is the End-User equipment installed in, as defined in ESS Table A27?"
    possible_values = DefaultValuesCertificateClimateZone
    default_value = DefaultValuesCertificateClimateZone.average_zone
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Which climate zone is the End-User equipment installed in, as defined in ESS Table A27?',
    }


""" These variables use Rule tables
"""
class HVAC2_equivalent_heating_hours_input(Variable):
    reference = 'table_F4.1'
    value_type = float
    entity = Building
    definition_period = ETERNITY 
    
    metadata = {
        "variable-type": "output"
    }
    
    def formula(building, period, parameters):
        climate_zone = building('HVAC2_certificate_climate_zone', period)
        heating_hours = parameters(period).ESS.HEAB.table_F4_1.heating_hours[climate_zone]
        return heating_hours


class HVAC2_equivalent_cooling_hours_input(Variable):
    reference = 'table_F4.1'
    value_type = float
    entity = Building
    definition_period = ETERNITY 
    metadata = {
        "variable-type": "output"
    }
    
    def formula(building, period, parameters):
        climate_zone = building('HVAC2_certificate_climate_zone', period)
        cooling_hours = parameters(period).ESS.HEAB.table_F4_1.cooling_hours[climate_zone]
        return cooling_hours


class HVAC2_baseline_ACOP_input(Variable):
    value_type = float
    entity = Building
    label = "Baseline ACOP"
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(building, period, parameters):
        cooling_capacity = building(
            'HVAC2_cooling_capacity_input', period)
        
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
        
        air_conditioner_type = building('HVAC2_Air_Conditioner_type', period)
        aircon = np.select(
            [air_conditioner_type == HVAC2_AC_Type.non_ducted_split_system, air_conditioner_type == HVAC2_AC_Type.ducted_split_system, air_conditioner_type == HVAC2_AC_Type.non_ducted_unitary_system, air_conditioner_type == HVAC2_AC_Type.ducted_unitary_system],
            
                ["non_ducted_split_system", "ducted_split_system", "non_ducted_unitary_system", "ducted_unitary_system"]
            )
        new_or_used_equipment = building('HVAC2_New_Equipment', period)
        
        
        baseline_acop = np.select(
            [new_or_used_equipment, np.logical_not(new_or_used_equipment)],
            
                [parameters(period).ESS.HEAB.table_F4_2.ACOP[aircon][cooling_capacity_to_check], 
                    parameters(period).ESS.HEAB.table_F4_3.ACOP[aircon][cooling_capacity_to_check] 
                    ]
            )

        return baseline_acop


class HVAC2_AC_Type(Enum):
    non_ducted_split_system = 'Non-ducted split system.'
    ducted_split_system = 'Ducted split system.'
    non_ducted_unitary_system = 'Non-ducted unitary system.'
    ducted_unitary_system = 'Ducted unitary system.'


class HVAC2_Air_Conditioner_type(Variable):
    value_type = Enum
    entity = Building
    label = "Air conditioner type"
    possible_values = HVAC2_AC_Type
    default_value = HVAC2_AC_Type.non_ducted_split_system
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'display_question' : 'What is your air conditioner type?',
        'sorting' : '4'
    }