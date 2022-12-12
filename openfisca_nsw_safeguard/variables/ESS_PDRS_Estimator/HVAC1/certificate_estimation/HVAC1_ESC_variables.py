import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for HVAC1 ESC Calculation
    These variables use GEMS Registry data
"""
class HVAC1_heating_capacity_input(Variable):
    reference = 'unit in kW'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Air Conditioner Heating Capacity",
        'display_question': 'Rated heating capacity at 7c as recorded in the GEMS Registry',
        'sorting' : 9,
        'label': 'Rated heated capacity (kW)'
    }


class HVAC1_cooling_capacity_input(Variable):
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


class HVAC1_rated_ACOP_input(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Rated ACOP",
        'display_question': 'Annual Coefficient of Performance (ACOP) as defined in the GEMS standard (air conditioners up to 65kW) Determination 2019',
        'sorting' : 11,
        'label': 'Rated ACOP'
    }


class HVAC1_baseline_AEER_input(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "AEER",
        "variable-type": "output",
        "label": "Baseline AEER"
    }

    def formula(building, period, parameters):
        cooling_capacity = building(
            'HVAC1_cooling_capacity_input', period)
        
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
        
        air_conditioner_type = building('HVAC1_Air_Conditioner_type', period)
        aircon = np.select(
            [air_conditioner_type == HVAC1_AC_Type.non_ducted_split_system, air_conditioner_type == HVAC1_AC_Type.ducted_split_system, air_conditioner_type == HVAC1_AC_Type.non_ducted_unitary_system, air_conditioner_type == HVAC1_AC_Type.ducted_unitary_system],
            
                ["non_ducted_split_system", "ducted_split_system", "non_ducted_unitary_system", "ducted_unitary_system"]
            )
       
        new_or_used_equipment = building('HVAC1_new_installation_activity', period)
        
        
        baseline_aeer = np.select(
            [new_or_used_equipment, np.logical_not(new_or_used_equipment)],
            
                [parameters(period).ESS.HEER.table_D16_2.AEER[aircon][cooling_capacity_to_check], 
                    parameters(period).ESS.HEER.table_D16_3.AEER[aircon][cooling_capacity_to_check] 
                    ]
            )

        return baseline_aeer


class HVAC1_rated_AEER_input(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Rated AEER",
        "display_question": 'Annual Energy Efficiency Ratio as defined in the GEMS Standards (Air Conditioners up to 65kW) Determination 2019',
        'sorting': 7,
        'label': 'Rated AEER'
    }
    
    
class HVAC1_certificate_climate_zone(Variable):
    value_type = int
    entity = Building
    label = "Which climate zone is the End-User equipment installed in, as defined in ESS Table A27?"
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'inter-interesting'
    }
    
    def formula(building, period, parameters):
        postcode = building('HVAC1_PDRS__postcode', period)
        rnf = parameters(period).ESS.ESS_general.table_A27_4_climate_zone_by_postcode
        zone_int = rnf.calc(postcode)
        return zone_int


class HVAC1_get_climate_zone_by_postcode(Variable):
    value_type = str
    entity = Building
    label = "Which climate zone is the End-User equipment installed in, as defined in ESS Table A27?"
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'inter-interesting',
        'alias': 'climate zone'
    }
    
    def formula(building, period, parameters):
        postcode = building('HVAC1_PDRS__postcode', period)
        rnf = parameters(period).ESS.ESS_general.table_A27_4_climate_zone_by_postcode
        zone_int = rnf.calc(postcode)
        climate_zone_str = np.select([zone_int == 1, zone_int == 2, zone_int == 3],
                                     ['hot', 'mixed', 'cold'])
        
        return climate_zone_str


class HVAC1_PDRS__postcode(Variable):
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


class HVAC1_residential_THEC(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY 
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'THEC (kWh/year)',
        'display_question' : 'The total annual heating energy consumption of the new air conditioner',
        'sorting' : 10
    }


class HVAC1_equivalent_heating_hours_input(Variable):
    reference = 'unit in hours per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }
    
    def formula(building, period, parameters):
        climate_zone = building('HVAC1_certificate_climate_zone', period)
        climate_zone_str = np.select([climate_zone == 1, climate_zone == 2, climate_zone == 3],
                                     ['hot_zone', 'average_zone', 'cold_zone'])
        heating_hours = parameters(period).ESS.HEER.table_D16_1.equivalent_heating_hours[climate_zone_str]
        return heating_hours


class HVAC1_residential_TCEC(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY 
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'TCEC (kWh/year)',
        'display_question' : 'The total annual cooling energy consumption of the new air conditioner',
        'sorting' : 6
    }


class HVAC1_equivalent_cooling_hours_input(Variable):
    reference = 'unit in hours per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(building, period, parameters):
        climate_zone = building('HVAC1_certificate_climate_zone', period)
        climate_zone_str = np.select([climate_zone == 1, climate_zone == 2, climate_zone == 3],
                                     ['hot_zone', 'average_zone', 'cold_zone'])
        cooling_hours = parameters(period).ESS.HEER.table_D16_1.equivalent_cooling_hours[climate_zone_str]
        return cooling_hours


class HVAC1_baseline_ACOP_input(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY

    def formula(building, period, parameters):
        cooling_capacity = building(
            'HVAC1_cooling_capacity_input', period)
        
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
        
        air_conditioner_type = building('HVAC1_Air_Conditioner_type', period)
        aircon = np.select(
            [air_conditioner_type == HVAC1_AC_Type.non_ducted_split_system, air_conditioner_type == HVAC1_AC_Type.ducted_split_system, air_conditioner_type == HVAC1_AC_Type.non_ducted_unitary_system, air_conditioner_type == HVAC1_AC_Type.ducted_unitary_system],
            
                ["non_ducted_split_system", "ducted_split_system", "non_ducted_unitary_system", "ducted_unitary_system"]
            )
        new_or_used_equipment = building('HVAC1_new_installation_activity', period)
        
        
        baseline_acop = np.select(
            [new_or_used_equipment, np.logical_not(new_or_used_equipment)],
            
                [parameters(period).ESS.HEER.table_D16_2.ACOP[aircon][cooling_capacity_to_check], 
                    parameters(period).ESS.HEER.table_D16_3.ACOP[aircon][cooling_capacity_to_check] 
                    ]
            )

        return baseline_acop


class HVAC1_AC_Type(Enum):
    non_ducted_split_system = 'Non-ducted split system'
    ducted_split_system = 'Ducted split system'
    non_ducted_unitary_system = 'Non-ducted unitary system'
    ducted_unitary_system = 'Ducted unitary system'


class HVAC1_Air_Conditioner_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = HVAC1_AC_Type
    default_value = HVAC1_AC_Type.non_ducted_split_system
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label': 'Air conditioner type',
        'display_question' : 'What is your air conditioner type?',
        'sorting' : 4
    }


class HVAC1_new_installation_activity(Variable):
    value_type = bool
    default_value = True
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'label' : 'Replacement or new installation activity',
        'display_question' : 'Is the activity an installation of a new high efficiency air conditioner?',
        'sorting' : 3
    }
    

class HVAC1_TCSPF_mixed(Variable):
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


class HVAC1_TCSPF_or_AEER_exceeds_ESS_benchmark(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Air Conditioner have a TCSPF mixed equal or greater than the minimum' \
            ' TCSPF mixed listed in Table D16.3? If the TCPSF is not available, is the Rated' \
            ' AEER equal or greater than the Minimum Rated AEER listed in Table D16.5?'
    metadata = {
        'alias':  'Air Conditioner has at least 5 years of Warranty'
    }

    def formula(buildings, period, parameters):
        AC_TCSPF = buildings('HVAC1_TCSPF_mixed', period)
        AC_AEER = buildings('HVAC1_rated_AEER_input', period)
        product_class = buildings('HVAC1_Air_Conditioner_type', period)
        # AC_Class = (product_class.possible_values)
        new_AC_cooling_capacity = buildings('HVAC1_cooling_capacity_input', period)
        cooling_capacity = np.select(
                                    [
                                        (new_AC_cooling_capacity < 4),
                                        ((new_AC_cooling_capacity >= 4) * (new_AC_cooling_capacity < 6)),
                                        ((new_AC_cooling_capacity >= 6) * (new_AC_cooling_capacity < 10)),
                                        ((new_AC_cooling_capacity >= 10) * (new_AC_cooling_capacity < 13)),
                                        ((new_AC_cooling_capacity >= 13) * (new_AC_cooling_capacity < 25)),
                                        ((new_AC_cooling_capacity >= 25) * (new_AC_cooling_capacity <= 65)),
                                        (new_AC_cooling_capacity > 65)
                                    ],
                                    [
                                        "less_than_4kW",
                                        "4kW_to_6kW",
                                        "6kW_to_10kW",
                                        "10kW_to_13kW",
                                        "13kW_to_25kW",
                                        "25kW_to_65kW",
                                        "over_65kW"
                                    ]
                                    )
        TCSPF_is_zero = ((AC_TCSPF == 0) + (AC_TCSPF == None))
        AC_exceeds_benchmark = np.where(
            TCSPF_is_zero,
            (AC_AEER >= parameters(period).PDRS.AC.table_D16_5[product_class][cooling_capacity]),
            (AC_TCSPF >= parameters(period).PDRS.AC.table_D16_4[product_class][cooling_capacity])
            )
        return AC_exceeds_benchmark


class HVAC1_HSPF_mixed(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'alias':  'Air Conditioner HSPF mixed',
        'label': 'Mixed HSPF',
        'display_question': 'Heating seasonal performance factor in an average climate zone'
    }


class HVAC1_HSPF_cold(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'alias':  'Air Conditioner HSPF cold',
        'label': 'Cold HSPF',
        'display_question': 'Heating seasonal performance factor in a cold climate zone'
    }

class HVAC1_HSPF_or_ACOP_exceeds_ESS_benchmark(Variable):
    """ This variable is used if the AC climate zone is hot or average and there is a GEMS heating capacity
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Air Conditioner have a HSPF mixed equal or greater than the minimum' \
            ' HSPF mixed listed in Table D16.3? If the HSPF is not available, is the Rated' \
            ' ACOP equal or greater than the Minimum Rated ACOP listed in Table D16.5?'
    metadata = {
        'alias':  'ESS - HSPF or ACOP exceeds benchmark'
    }

    def formula(buildings, period, parameters):
        AC_HSPF_mixed = buildings('HVAC1_HSPF_mixed', period)
        AC_HSPF_cold = buildings('HVAC1_HSPF_cold', period)
        AC_ACOP = buildings('HVAC1_rated_ACOP_input', period)
        product_class = buildings('HVAC1_Air_Conditioner_type', period)
        new_AC_cooling_capacity = buildings('HVAC1_cooling_capacity_input', period)
        cooling_capacity = np.select(
                                    [
                                        (new_AC_cooling_capacity < 4),
                                        ((new_AC_cooling_capacity >= 4) * (new_AC_cooling_capacity < 6)),
                                        ((new_AC_cooling_capacity >= 6) * (new_AC_cooling_capacity < 10)),
                                        ((new_AC_cooling_capacity >= 10) * (new_AC_cooling_capacity < 13)),
                                        ((new_AC_cooling_capacity >= 13) * (new_AC_cooling_capacity < 25)),
                                        ((new_AC_cooling_capacity >= 25) * (new_AC_cooling_capacity <= 65)),
                                        (new_AC_cooling_capacity > 65)
                                    ],
                                    [
                                        "less_than_4kW",
                                        "4kW_to_6kW",
                                        "6kW_to_10kW",
                                        "10kW_to_13kW",
                                        "13kW_to_25kW",
                                        "25kW_to_65kW",
                                        "over_65kW"
                                    ]
                                    )

        climate_zone = buildings('HVAC1_certificate_climate_zone', period)
        climate_zone_str = np.select([climate_zone == 1, climate_zone == 2, climate_zone == 3],
                                     ['hot_zone', 'average_zone', 'cold_zone'])

        in_hot_zone = (climate_zone_str == 'hot_zone')
        in_average_zone = (climate_zone_str == 'average_zone')
        in_cold_zone = (climate_zone_str == 'cold_zone')

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
        AC_exceeds_benchmark = np.select([
                                            HSPF_is_zero,
                                            np.logical_not(HSPF_is_zero) * in_cold_zone,
                                            np.logical_not(HSPF_is_zero) * np.logical_not(in_cold_zone),
                                            ],
                                            [
            (AC_ACOP >= parameters(period).ESS.HEER.table_D16_5['ACOP'][product_class][cooling_capacity]),
            (AC_HSPF >= parameters(period).ESS.HEER.table_D16_4['HSPF_cold'][product_class][cooling_capacity]),
            (AC_HSPF >= parameters(period).ESS.HEER.table_D16_4['HSPF_mixed'][product_class][cooling_capacity])
                                            ]
            )
        return AC_exceeds_benchmark