from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np

from openfisca_nsw_safeguard.regulation_reference import ESS_2021


class ESS__HEER_TypeOfInsulation(Enum):
  ceiling_insulation = 'Insulation installed is ceiling insulation.'
  underfloor_insulation = 'Insulation installed is underfloor insulation.'
  wall_insulation = 'Insulation installed is wall insulation.'


class ESS__HEER_type_of_insulation(Variable):
    value_type = Enum
    entity = Building
    possible_values = ESS__HEER_TypeOfInsulation
    default_value = ESS__HEER_TypeOfInsulation.ceiling_insulation
    definition_period = ETERNITY
    label = 'Is there existing insulation in the ceiling space?'
    metadata = {
        'alias': "ESS Insulation - Type of Insulation Installed",
        "regulation_reference": ESS_2021["8", "8.8"]
    }


class ESS__HEER_insulation_existing_insulation(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is there existing insulation in the ceiling space?'
    metadata = {
        'alias': "ESS Insulation - Existing Insulation in Ceiling Space",
        "regulation_reference": ESS_2021["8", "8.8"]
    }


class ESS__HEER_insulation_meets_AS4859_performance_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the insulation meet the performance requirements defined in AS4859.1?'
    metadata = {
        'alias': "ESS Insulation - Meets AS4859.1 Requirements",
         "regulation_reference": ESS_2021["8", "8.8"]
   }


class ESS__HEER_insulation_warranty_length(Variable):
    value_type = int
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the length of the insulation\'s warranty, in years?'
    metadata = {
        'alias': "ESS Insulation - Insulation Warranty Length",
        "regulation_reference": ESS_2021["8", "8.8"]
}

class ESS__HEER_insulation_is_foil(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the installed insulation foil?'
    metadata = {
        'alias': "ESS Insulation - Installed Insulation Is Foil",
        "regulation_reference": ESS_2021["8", "8.8"]
    }


class ESS__HEER_insulation_R_value(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What is the R Value of the installed insulation?'
    metadata = {
        'alias': "ESS Insulation - Installed Insulation R Value",
        "regulation_reference": ESS_2021["8", "8.8"]
    }


class ESS__HEER_insulation_meets_minimum_R_value(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the insulation implementation meet all of the Equipment' \
            ' Requirements?'
    metadata = {
        'alias': "Install insulation meets equipment requirements",
        "regulation_reference": ESS_2021["8", "8.8"]
    }

    def formula(buildings, period, parameters):
        type_of_insulation = buildings(
            'ESS__HEER_type_of_insulation', period)
        BCA_climate_zone = buildings(
            'ESS__BCA_climate_zone', period)
