from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

from openfisca_nsw_safeguard.variables.ESS_lighting_common_variables import LightingEquipmentClass

class ESS_HEER_lighting_existing_lamp_type(Variable):
    value_type = Enum
    possible_values = LightingEquipmentClass
    default_value = LightingEquipmentClass.T12_linear
    entity = Building
    definition_period = ETERNITY
    label = 'Defines the existing lamp type, as defined in Table A9.1 or Table A9.3' \
            ' in Schedule A.'


class ESS_HEER_lighting_new_lamp_type(Variable):
    value_type = Enum
    possible_values = LightingEquipmentClass
    default_value = LightingEquipmentClass.T12_linear
    entity = Building
    definition_period = ETERNITY
    label = 'Defines the new lamp type, as defined in Table A9.1 or Table A9.3' \
            ' in Schedule A.'


class ESS_HEER_lighting_existing_lamp_circuit_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Allows the user to input the Lamp Circuit Power for the new lamp' \
            'in W, as measured in accordance with Table A9.4.'


class ESS_HEER_existing_lamp_rating(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the rated wattage of the existing lamp.'  # need to check whether lamp rating is int or float


class ESS_HEER_existing_lamp_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the length of the existing lamp, in millimetres?'


class ESS_HEER_number_of_existing_lamps(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'How many lamps are in the existing luminaire?'


class ESS_HEER_lighting_new_lamp_circuit_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Allows the user to input the Lamp Circuit Power for the new lamp' \
            'in W, as measured in accordance with Table A9.4.'


class ESS_HEER_new_lamp_life(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'measures the Lamp Life of the replacement light in hours'


class ESS_HEER_lighting_new_lamp_light_output(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the light output of the new lamp?'


class ESS_HEER_new_lamp_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the length of the new lamp, in millimetres?'


class ESS_HEER_downward_light_output(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'User input for the downward light output of the new End-User' \
            ' Equipment, in lumens.'


class ESS_HEER_original_light_beam_angle(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'user input for the angle of the original lamp light beam.'


class ESS_HEER_new_light_beam_angle(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'user input for the angle of the new lamp light beam.'
