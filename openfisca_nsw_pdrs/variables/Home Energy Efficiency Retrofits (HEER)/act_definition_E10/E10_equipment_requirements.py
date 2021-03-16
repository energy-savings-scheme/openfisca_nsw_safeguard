# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class new_equipment_is_external_shading_device(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new product is an external shading device' \
            ' as prescribed in Equipment Requirement 1.'


class new_equipment_is_automated(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new product is automated.'


class E10_warranty_length(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the warranty length of the blind, in years.'


class E10_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the blind has a minimum warranty length of' \
            ' 5 years, as required by Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('E10_warranty_length', period)
        return warranty_length >= 5
