# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class existing_lamp_is_240V_PAR(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp is a 240V parabolic aluminised' \
            ' reflector lamp, as required in Eligiblity Requirement 1 in' \
            ' Activity Definition E3, and defined in Table A9.1.'  # this light type is not defined anywhere in the rule (and probably should be!)


class E3_existing_lamp_rating(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the rated wattage of the existing lamp.'  # need to check whether lamp rating is int or float


class existing_lamp_rating_more_than_80W_less_than_160W(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp rating is 35W or 50W, as required' \
            ' in Eligibility Requirement 3 in Activity Definition E1.'  # need to check if this is inclusive or not

    def formula(buildings, period, parameters):
        existing_lamp_rating = buildings('existing_lamp_rating', period)
        return existing_lamp_rating > 80 and existing_lamp_rating < 160


class E3_is_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the existing lamp and luminaire is in working order' \
            ' as required in Eligibility Requirement 3 in Activity Definition' \
            ' E1.'  # insert definition requirements
