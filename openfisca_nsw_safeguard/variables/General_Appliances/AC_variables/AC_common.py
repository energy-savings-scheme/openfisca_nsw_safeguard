import numpy as np
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_core.variables import Variable
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021


class AC_Type(Enum):
    non_ducted_split_system = 'The AC is a non-ducted split system.'
    ducted_split_system = 'The AC is a ducted split system.'
    non_ducted_unitary_system = 'The AC is a non-ducted split system.'
    ducted_unitary_system = 'The AC is a ducted split system.'


class Air_Conditioner_type(Variable):
    # name="AC Type as defined in GEMS or MEPS"
    reference = "GEMS or MEPS"
    value_type = Enum
    possible_values = AC_Type
    default_value = AC_Type.non_ducted_split_system
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Air Conditioner Type",
        "regulation_reference": ESS_2021["XX", "AC"]
    }


class AC_cooling_capacity(Enum):
    less_than_4 = "cooling capacity < 4kW"
    between_4_and_10 = "4kw =< cooling capacity < 10kW"
    between_10_and_39 = "10kw =< cooling capacity < 39kW"
    between_39_and_65 = "39kw =< cooling capacity < 65kW"
    more_than_65 = "cooling capacity >= 65kW"


class Air_Conditioner__cooling_capacity(Variable):
    reference = "unit in kw"
    value_type = float
    entity = Building
    label = "What is the product cooling capacity in the label?"
    definition_period = ETERNITY
    metadata = {
        "alias": "Air Conditioner Cooling Capacity",
        "regulation_reference": ESS_2021["XX", "AC"]
    }


class AC_cooling_capacity_enum(Variable):
    value_type = Enum
    entity = Building
    label = "What is the product cooling capacity Enum used to look up the table?"
    definition_period = ETERNITY
    possible_values = AC_cooling_capacity
    default_value = AC_cooling_capacity.less_than_4
    metadata = {
        "alias": "Air Conditioner Cooling Capacity Enum",
        "regulation_reference": ESS_2021["XX", "AC"]
    }

    def formula(building, period):
        cooling_capacity = building(
            'Air_Conditioner__cooling_capacity', period)
        return np.select(
            [
                cooling_capacity < 4,
                (cooling_capacity < 10) & (cooling_capacity >= 4),
                (cooling_capacity < 39) & (cooling_capacity >= 10),
                (cooling_capacity < 65) & (cooling_capacity >= 39),
                cooling_capacity > 65
            ],
            [
                AC_cooling_capacity.less_than_4,
                AC_cooling_capacity.between_4_and_10,
                AC_cooling_capacity.between_10_and_39,
                AC_cooling_capacity.between_39_and_65,
                AC_cooling_capacity.more_than_65
            ])


class AC_heating_capacity(Enum):
    less_than_4 = "heating capacity < 4kW"
    between_4_and_10 = "4kw =< heating capacity < 10kW"
    between_10_and_39 = "10kw =< heating capacity < 39kW"
    between_39_and_65 = "39kw =< heating capacity < 65kW"
    more_than_65 = "heating capacity >= 65kW"


class Air_Conditioner__heating_capacity(Variable):
    reference = "unit in kw"
    value_type = float
    entity = Building
    label = "What is the product heating capacity in the label?"
    definition_period = ETERNITY
    metadata = {
        "alias": "Air Conditioner heating Capacity",
        "regulation_reference": ESS_2021["XX", "AC"]
    }


class AC_heating_capacity_enum(Variable):
    value_type = Enum
    entity = Building
    label = "What is the product heating capacity Enum used to look up the table?"
    definition_period = ETERNITY
    possible_values = AC_heating_capacity
    default_value = AC_heating_capacity.less_than_4
    metadata = {
        "alias": "Air Conditioner Heating Capacity Enum",
        "regulation_reference": ESS_2021["XX", "AC"]
    }

    def formula(building, period):
        heating_capacity = building(
            'Air_Conditioner__heating_capacity', period)
        return np.select(
            [
                heating_capacity < 4,
                (heating_capacity < 10) & (heating_capacity >= 4),
                (heating_capacity < 39) & (heating_capacity >= 10),
                (heating_capacity < 65) & (heating_capacity >= 39),
                heating_capacity > 65
            ],
            [
                AC_heating_capacity.less_than_4,
                AC_heating_capacity.between_4_and_10,
                AC_heating_capacity.between_10_and_39,
                AC_heating_capacity.between_39_and_65,
                AC_heating_capacity.more_than_65
            ])



class AC_TCSPF_mixed(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the TCSPF mixed for the AC, as listed in the GEMS Registry?'
    metadata = {
    'alias':  'Air Conditioner TCSPF',
    "regulation_reference": PDRS_2022["XX", "AC"]
}


class AC_HSPF_mixed(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the HSPF mixed for the AC, as listed in the GEMS Registry?'
    metadata = {
    'alias':  'Air Conditioner HSPF mixed',
}


class AC_HSPF_cold(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the HSPF cold for the AC, as listed in the GEMS Registry?'
    metadata = {
    'alias':  'Air Conditioner HSPF cold',
}


class AC_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the input power for the AC, as listed in the GEMS Registry?'
    metadata = {
    'alias':  'Air Conditioner input power',
}


class AC_AEER(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the AEER for the AC, as listed in the GEMS Registry?'
    metadata = {
    'alias':  'Air Conditioner TCSPF',
    "regulation_reference": PDRS_2022["XX", "AC"]
}


class AC_ACOP(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the AEER for the AC, as listed in the GEMS Registry?'
    metadata = {
    'alias':  'Air Conditioner TCSPF',
    "regulation_reference": PDRS_2022["XX", "AC"]
}


class ACClimateZone(Enum):
    hot_zone = "AC is installed in the hot zone."
    average_zone = "AC is installed in the average zone."
    cold_zone = "AC is installed in the cold zone."


class AC_climate_zone(Variable):
    value_type = Enum
    entity = Building
    label = "What is the climate zone the end-user equipment is installed in?"
    definition_period = ETERNITY
    possible_values = ACClimateZone
    default_value = ACClimateZone.average_zone
    metadata = {
        "alias": "Air Conditioner Climate Zone",
        "regulation_reference": ESS_2021["XX", "AC"],
        'display_question':"Which climate zone is the End-User equipment installed in, as defined in ESS Table A27?"
    }

class HVAC_2_TCPSF_greater_than_minimum(Variable):
    value_type = bool
    entity = Building
    label = 'Is your TCPSF equal to or greater than the Minimum for the same Product Type and Cooling Capacity?'
    metadata = {
        'display_question' : 'Is your TCPSF equal to or greater than the Minimum TCPSF for the same Product Type and Cooling Capacity in ESS Table F4.5?'
    }

class HVAC_2_AEER_greater_than_minimum(Variable):
    value_type = bool
    entity = Building
    label = 'Is your AEER equal to or greater than the Minimum for the same Product Type and Cooling Capacity?'
    metadata = {
        'display_question' : 'Is your AEER equal to or greater than the Minimum AEER for the same Product Type and Cooling Capacity in ESS Table F4.4?'
    }

