# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class E2_placeholder(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Equation 1 of the ESS Rule 2009, used to calculate the number' \
            ' of ESCs generated from a Recognised Energy Savings Activity.' \
            ' As defined in Clause 6.5 of the ESS Rule 2009.'
