import numpy as np
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_core.variables import Variable
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021


class AC_Type(Enum):
    type_1 = 'Wall mounted, unitary, and double duct'
    type_2 = 'Portable, unitary, and double duct'
    type_3 = 'Wall mounted, unitary, and single duct'
    type_4 = 'Portable, unitary, and single duct'
    type_5 = 'Air to air unitary, ducted or non-ducted, excluding classes 1 to 4'
    type_6 = 'Air to air single split system, non-ducted'
    type_7 = 'Air to air single split system, ducted'
    type_8 = 'Air to air single split outdoor units, supplied or offered for supply to create a non-ducted system'
    type_9 = 'Air to air single split outdoor units, supplied or offered for supply to create a ducted system'
    type_10 = 'Air to air multi-split outdoor units, whether or not supplied or offered for supply as part of a multi-split system​'


class Air_Conditioner_type(Variable):
    # name="AC Type as defined in GEMS or MEPS"
    reference = "GEMS or MEPS"
    value_type = Enum
    possible_values = AC_Type
    default_value = AC_Type.type_6
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "Air Conditioner Type",
        "regulation_reference": ESS_2021
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
        "regulation_reference": ESS_2021
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
        "regulation_reference": ESS_2021
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
