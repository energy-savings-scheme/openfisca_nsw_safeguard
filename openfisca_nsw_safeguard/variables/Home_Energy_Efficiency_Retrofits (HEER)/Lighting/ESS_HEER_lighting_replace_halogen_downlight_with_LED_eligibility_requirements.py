from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class existing_lamp_is_tungsten_halogen_240V_or_ELV_or_infrafred_ELV(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a Infrared Coated Halogen Lamp, as' \
            ' required in Eligiblity Requirement 1 in Activity Definition' \
            ' E1, and defined in Table A9.1.'  # insert definition requirements

    def formula(buildings, period, parameters):
        existing_lamp_type = buildings('existing_lamp_type', period)
        EquipmentClassStatus = existing_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_tungsten_halogen_240V = (existing_lamp_type == EquipmentClassStatus.tungsten_halogen_240V)
        is_tungsten_halogen_ELV = (existing_lamp_type == EquipmentClassStatus.tungsten_halogen_ELV)
        is_infrared_coated_ELV = (existing_lamp_type == EquipmentClassStatus.infrared_coated_ELV)
        return is_tungsten_halogen_240V + is_tungsten_halogen_ELV + is_infrared_coated_ELV


class is_multifacted_reflector(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the lamp is a multifaceted reflector lamp, as' \
            ' required in Eligibility Requirement 2 in Activity Definition' \
            ' E1.'  # insert definition requirements


class E1_existing_lamp_rating(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the rated wattage of the existing lamp.'  # need to check whether lamp rating is int or float


class existing_lamp_rating_is_35W_or_50W(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp rating is 35W or 50W, as required' \
            ' in Eligibility Requirement 3 in Activity Definition E1.'  # insert definition requirements

    def formula(buildings, period, parameters):
        existing_lamp_rating = buildings('existing_lamp_rating', period)
        condition_lamp_rating = existing_lamp_rating == 35 or existing_lamp_rating == 50
        return where(condition_lamp_rating, True, False)


class is_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp and luminaire is in working order' \
            ' as required in Eligibility Requirement 3 in Activity Definition' \
            ' E1.'  # insert definition requirements
