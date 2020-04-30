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
    BCA_Climate_Zone_4 = 'Implementation takes place in BCA Climate Zone 4.' \
    BCA_Climate_Zone_5 = 'Implementation takes place in BCA Climate Zone 5.' \
    BCA_Climate_Zone_6 = 'Implementation takes place in BCA Climate Zone 6.' \
    BCA_Climate_Zones_7_and_8 = 'Implementation takes place in BCA Climate' \
                                ' Zone 7 or BCA Climate Zone 8.'

class BCA_climate_zone(Variable):
    value_type = Enum
    possible_values = BCAClimateZone
    default_value = BCAClimateZone.BCA_Climate_Zones_2_and_3
    entity = Building
    definition_period = ETERNITY
    label = 'Defines what Climate Zone, as defined by the BCA, the' \
            ' Implementation is conducted within.'
