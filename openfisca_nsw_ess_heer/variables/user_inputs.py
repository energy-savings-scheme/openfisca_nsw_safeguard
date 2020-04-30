# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class new_lamp_circuit_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Allows the user to input the Lamp Circuit Power for the new lamp' \
            'in W, as measured in accordance with Table A9.4.'


class new_lamp_light_output(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Allows the user to input the light output for the new lamp' \
            'in lm, as measured in accordance with Table A9.4.'


class existing_lamp_LCP(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Allows the user to input the Lamp Circuit Power for the new lamp' \
            'in W, as measured in accordance with Table A9.4.'


class BCAClimateZone(Enum):
    BCA_Climate_Zones_2_and_3 = 'Implementation takes place in BCA Climate' \
                                ' Zone 2 or BCA Climate Zone 3.'
    BCA_Climate_Zone_4 = 'Implementation takes place in BCA Climate Zone 4.'
    BCA_Climate_Zone_5 = 'Implementation takes place in BCA Climate Zone 5.'
    BCA_Climate_Zone_6 = 'Implementation takes place in BCA Climate Zone 6.'
    BCA_Climate_Zones_7_and_8 = 'Implementation takes place in BCA Climate' \
                                ' Zone 7 or BCA Climate Zone 8.'


class BCA_Climate_Zone(Variable):
    value_type = Enum
    possible_values = BCAClimateZone
    default_value = BCAClimateZone.BCA_Climate_Zones_2_and_3
    entity = Building
    definition_period = ETERNITY
    label = 'Defines what Climate Zone, as defined by the BCA, the' \
            ' Implementation is conducted within.'


class BuildingType(Enum):
    residential_building = 'Implementation takes place on a Residential' \
                           ' Building, which means a building or part of a' \
                           ' building classified as a BCA Class 1, 2 or 4' \
                           ' building, and may include any Non-Habitable' \
                           ' Building on the same site.'
    small_business_site = 'Implementation takes place on a Small Business' \
                          ' Site, which is defined as a Site that (a) is' \
                          ' entirely occupied by one business; and (b) where' \
                          ' the business, as a consumer of electricity at' \
                          ' the Site: i. is a Small Customer (and, for the' \
                          ' avoidance of doubt, has not aggregated its load' \
                          ' at the Site with consumption at other Sites for' \
                          ' the purposes of being treated as a Large' \
                          ' Customer under its electricity purchase' \
                          ' arrangements); or ii.	is a customer of an Exempt' \
                          ' Seller, and has an annual electricity consumption' \
                          ' below the Upper Consumption Threshold for' \
                          ' electricity.'


class building_type(Variable):
    value_type = Enum
    possible_values = BuildingType
    default_value = BuildingType.residential_building
    entity = Building
    definition_period = ETERNITY
    label = 'Defines what building type the Implementation is conducted within.'
