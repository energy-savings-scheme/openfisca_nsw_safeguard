from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class RF1_removal(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the removal of a spare non-primary refrigerator or freezer at the site?',
      'sorting' : 1,
      'eligibility_clause' : """In PDRS RF1 Equipment Requirements Clause 6 it states that as a result of the activity there must be 1 fewer spare refrigerators and freezers at the Site."""
    }


class RF1_primary_refrigeration(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is there another refrigerator or freezer on site that provides primary refrigeration or freezing services, located in, or closer to, the kitchen?',
      'sorting' : 2,
      'eligibility_clause' : """In PDRS RF1 Equipment Requirements Clause 5 it states that there must be another Refrigerator or Freezer (as appropriate) at the Site that provides primary refrigeration or freezing services, located in, or closer to, the kitchen."""
    }


class RF1_residential_building(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User equipment located in a residential building?',
      'sorting' : 3,
      'eligibility_clause' : """In PDRS RF1 Equipment Requirements Clause 1 it states that the Site where the End-User Equipment is located must be a Residential Building."""
    }


class RF1_in_working_order(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User equipment in working order?',
      'sorting' : 4,
      'eligibility_clause' : """In PDRS RF1 Equipment Requirements Clause 4 it states that the Refrigerator or Freezer must be in working order."""
    }


class RF1_classified_group(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User equipment classified as Group 1, 2, 3, 4, 5T, 5B, 5S, 6C, 6U or 7 according to AS/NZS 4474.1 and 4474.2 Performance of household electrical appliances—Refrigerating appliances?',
      'sorting' : 5,
      'eligibility_clause' : """In PDRS RF1 Equipment Requirements Clause 2 it states that the End-User Equipment must be a Refrigerator or Freezer (or combination) that may be classified as Group 1, 2, 3, 4, 5T, 5B, 5S, 6C, 6U or 7 according to AS/NZS 4474.1 and 4474.2 Performance of household electrical appliances—Refrigerating appliances."""
    }


class RF1_capacity_200_litres_or_more(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the capacity of the refrigerator or freezer 200 litres or more?',
      'sorting' : 6,
      'eligibility_clause' : """In PDRS RF1 Equipment Requirements Clause 3 it states that the capacity of the Refrigerator or Freezer (as defined in AS/NZS 4474) must be 200 litres or more."""
    }