# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class new_equipment_is_240V_edison_screw_or_bayonet_self_ballasted_LED(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new product is an external shading device' \
            ' as prescribed in Equipment Requirement 1.'


class mew_equipment_meets_requirements_of_A9_4(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new product meets the requirements of Table A9.4' \
            ' as prescribed by Equipment Requirement 2.'  # IPART to define what meeting these requirements means


class new_equipment_compatible_with_installed_dimmer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new equipment is compatible with any dimmer' \
            ' installed on the same circuit as the new equipment, as prescribed' \
            ' by Equipment Requirement 3.'


class new_lamp_light_output_greater_or_equal_to_existing_light_output(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new product has the same or higher light output' \
            ' as the existing lamp in lumens, as required by Equipment' \
            ' Requirement 4.'

    def formula(buildings, period, parameters):
        existing_light_output = buildings('existing_lamp_light_output', period)
        new_light_output = buildings('new_lamp_light_output', period)
        return new_light_output >= existing_light_output
