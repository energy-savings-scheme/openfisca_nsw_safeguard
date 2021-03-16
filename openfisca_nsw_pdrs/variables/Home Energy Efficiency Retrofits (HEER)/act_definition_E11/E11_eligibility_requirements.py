# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class existing_lamp_is_240v_fixed_ceiling_or_wall_mounted_luminaire(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a 240V fixed ceiling or wall' \
            ' mounted luminaire, as required in Eligiblity Requirement 1' \
            ' in Activity Definition E10.'  # insert definition requirements. note these are not defined in A9.1 or A9.3


class existing_lamp_is_edison_screw_or_bayonet_lamp(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is an Edison Screw or bayonet lamp' \
            ' as required in Eligiblity Requirement 2 in Activity' \
            ' Definition E10.'  # insert definition requirements. note these are not defined in A9.1 or A9.3


class existing_lamp_is_incandescent_halogen_or_CFL(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is an incandescent, halogen or' \
            ' CFL lamp as required in Eligiblity Requirement 3 in Activity' \
            ' Definition E10.'  # insert definition requirements. note these are not defined in A9.1 or A9.3


class existing_lamp_is_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is in working order, as required' \
            ' in Eligiblity Requirement 4 in Activity Definition E10.'  # insert definition requirements. note these are not defined in A9.1 or A9.3


class replacement_is_lamp_only(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the replacement activity is for the lamp only' \
            ' as required in Eligiblity Requirement 5 in Activity Definition E10.'  # insert definition requirements. note these are not defined in A9.1 or A9.3
