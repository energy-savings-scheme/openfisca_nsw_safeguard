# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class new_equipment_can_be_closed_to_seal_exhaust(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new product is a self-closing damper, flap or' \
            ' other sealing product that can be closed to seal the exhaust' \
            ' of a fan, as prescribed by Equipment Requirement 1.'


class egress_of_air_is_allowed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new product allows the egress of air when the' \
            ' exhaust fan is in operation, as prescribed by Equipment' \
            ' Requirement 2.'  # IPART to define what meeting these requirements means


class E12_warranty_length(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the warranty length of the blind, in years.'


class E12_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the blind has a minimum warranty length of' \
            ' 5 years, as required by Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('E12_warranty_length', period)
        return warranty_length >= 2
