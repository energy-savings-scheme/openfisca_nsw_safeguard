from openfisca_core.variables import Variable, Enum, ETERNITY
import openfisca_nsw_pdrs.variables.PDRS_AirConditioner.appliance_entity as appliance_entity


class AC_Type(Enum):
    type_1 = 'Wall mounted, unitary, and double duct'
    type_2 = 'Portable, unitary, and double duct'
    type_3 = 'Wall mounted, unitary, and single duct'
    type_4 = 'Portable, unitary, and single duct'
    type_5 = 'Air to air unitary, ducted or non-ducted, excluding classes 1 to 4'
    type_6 = 'Air to air single split system, non-ducted'
    type_7 = 'Air to air single split system, ducted'
    type_8='Air to air single split system, ducted or non-ducted'
    type_9='Air to air single split outdoor units, supplied or offered for supply to create a non-ducted system'
    type_10='Air to air single split outdoor units, supplied or offered for supply to create a ducted system'
    type_11='Air to air single split outdoor units, whether supplied or offered for supply to create a ducted or non-ducted system'
    type_12='Air to air multi-split outdoor units, whether or not supplied or offered for supply as part of a multi-split system​'

class PDRS__Air_Conditioner__AC_Type(Variable):
    # name="AC Type as defined in GEMS or MEPS"
    reference="GEMS or MEPS"
    value_type=Enum
    possible_values=AC_Type
    default_value=AC_Type.type_6
    entity=appliance_entity.Appliance
    definition_period=ETERNITY

# TODO: think about how to code up the table

class PDRS__Air_Conditioner__cooling_capacity(Variable):
    # name="Air Conditioner Cooling Capacity in kW"
    reference="unit in kw"
    value_type=float
    entity=appliance_entity.Appliance
    label="What is the product cooling capacity in the label?"
    definition_period=ETERNITY



# TODO: how to combine the Enums with the variable that uses it

class installation_type(Enum):
    new="Installation of a new product"
    replacement="Replacement of an old product"

class PDRS__Appliance__installation_type(Variable):
    # name="New or Replacement?"
    reference=""
    value_type=Enum
    possible_values=installation_type
    default_value=installation_type.new
    entity=appliance_entity.Appliance
    definition_period=ETERNITY
    label="Is it a new installation or a replacement?"



class PDRS__Air_Conditioner__baseline_power_input(Variable):
    value_type = float
    entity = appliance_entity.Appliance
    label = 'returns the baseline power input for an Air Conditioner'
    definition_period=ETERNITY


    def formula(appliance, period):
        # install_type=appliance('installation_type', period)
        cooling_capacity = appliance('PDRS__Air_Conditioner__cooling_capacity', period)
        return cooling_capacity



# formula = PDRS__Air_Conditioner__baseline_power_input.get_formula(period=None)
# is_input = PDRS__Air_Conditioner__baseline_power_input.is_input_variable()

# print(formula)
# print(is_input)