import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class F17_installation(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the equipment being installed an air source heat pump water heater as defined by AS/NZS 4234?',
      'sorting' : 1,
      'eligibility_clause' : """In ESS F17 the activity definition states that the New End-User Equipment must be an air source heat pump water heater as defined by AS/NZS 4234."""
    }


    class F17_licensed_person(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Has installation of the new equipment been performed or supervised by a suitably licensed person?',
      'sorting' : 2,
      'eligibility_clause' : """In ESS F17 the activity definition states that The activity must be performed or supervised by a suitably qualified licence holder in compliance with the relevant standards and legislation."""
    }
    testing 
    