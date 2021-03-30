import numpy as np

from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

class AC_Type(Enum):
    type_1 = 'Wall mounted, unitary, and double duct'
    type_2 = 'Portable, unitary, and double duct'
    type_3 = 'Wall mounted, unitary, and single duct'
    type_4 = 'Portable, unitary, and single duct'
    type_5 = 'Air to air unitary, ducted or non-ducted, excluding classes 1 to 4'
    type_6 = 'Air to air single split system, non-ducted'
    type_7 = 'Air to air single split system, ducted'
    type_8='Air to air single split outdoor units, supplied or offered for supply to create a non-ducted system'
    type_9='Air to air single split outdoor units, supplied or offered for supply to create a ducted system'
    type_10='Air to air multi-split outdoor units, whether or not supplied or offered for supply as part of a multi-split system​'


class PDRS__Air_Conditioner__AC_type(Variable):
    # name="AC Type as defined in GEMS or MEPS"
    reference="GEMS or MEPS"
    value_type=Enum
    possible_values=AC_Type
    default_value=AC_Type.type_6
    entity=Building
    definition_period=ETERNITY
    metadata={
        "variable-type": "input",
        "alias":"Air Conditioner Type",
        "activity-group":"PDRS: Air Conditioner",
        "activity-name":"Installation or Replacement of an Air Conditioner"
        }


class AC_cooling_capacity(Enum):
    less_than_4="cooling capacity < 4kW"
    between_4_and_10="4kw =< cooling capacity < 10kW"
    between_10_and_39="10kw =< cooling capacity < 39kW"
    between_39_and_65="39kw =< cooling capacity < 65kW"
    more_than_65="cooling capacity >= 65kW"



class PDRS__Air_Conditioner__cooling_capacity(Variable):
    # name="Air Conditioner Cooling Capacity in kW"
    reference="unit in kw"
    value_type=float
    # possible_values=AC_cooling_capacity
    # default_value=AC_cooling_capacity.less_than_4
    entity=Building
    label="What is the product cooling capacity in the label?"
    definition_period=ETERNITY
    metadata={
        "variable-type": "input",
        "alias":"Air Conditioner Cooling Capacity",
        "activity-group":"PDRS: Air Conditioner",
        "activity-name":"Installation or Replacement of an Air Conditioner"
        }




class installation_type(Enum):
    new="Installation of a new product"
    replacement="Replacement of an old product"

class PDRS__Appliance__installation_type(Variable):
    # name="New or Replacement?"
    reference=""
    value_type=Enum
    possible_values=installation_type
    default_value=installation_type.new
    entity=Building
    definition_period=ETERNITY
    label="Is it a new installation or a replacement?"
    metadata={
        "variable-type": "input",
        "alias":"New or Replacement?",
        "activity-group":"PDRS: Air Conditioner",
        "activity-name":"Installation or Replacement of an Air Conditioner"
        }


class PDRS__Air_Conditioner__baseline_power_input(Variable):
    value_type = float
    entity = Building
    label = 'returns the baseline power input for an Air Conditioner'
    definition_period=ETERNITY
    metadata={
        "variable-type": "intermediary",
        "alias" :"Baseline Power Input",
        "activity-group":"PDRS: Air Conditioner",
        "activity-name":"Installation or Replacement of an Air Conditioner"
        }



    def formula(building, period, parameters):
        cooling_capacity = building('PDRS__Air_Conditioner__cooling_capacity', period)

        cooling_capacity_enum=np.select(
            [
                cooling_capacity < 4,
                (cooling_capacity < 10) & (cooling_capacity >= 4),
                (cooling_capacity < 39) & (cooling_capacity >= 10),
                (cooling_capacity < 65) & (cooling_capacity >= 39),
                cooling_capacity>65
            ],
            [
                AC_cooling_capacity.less_than_4,
                AC_cooling_capacity.between_4_and_10,
                AC_cooling_capacity.between_10_and_39,
                AC_cooling_capacity.between_39_and_65,
                AC_cooling_capacity.more_than_65
            ])


        replace_or_new = building('PDRS__Appliance__installation_type', period)
        AC_type = building('PDRS__Air_Conditioner__AC_type', period)
        baseline_unit=parameters(period).AC_baseline_power_per_capacity_reference_table[replace_or_new]
        scale = baseline_unit[AC_type]

        return scale[cooling_capacity_enum]*cooling_capacity
