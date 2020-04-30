# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E8_windows_have_gaps_between_door_and_frame(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Windows to be draught-proofed must have gaps between the door and' \
            ' frame and/or threshold that permit the infiltration of air into' \
            ' or out of the Site. Prescribed by Equipment Requirement 1 of' \
            ' Energy Savings Scheme Rule 2020.'  # IPART to define what this means and how to measure this


class window_is_external(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Only external doors may be draught-proofed. Prescribed by' \
            ' Equipment Requirement 1 of Energy Savings Scheme Rule 2020.'
