from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class product_applied_to_door_bottom_seal(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Product is applied to door bottom seal.'


class product_applied_to_set_door_jamb(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Product is applied to set door jamb.'


class product_applied_to_head_seals(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Product is applied to door head seals.'


class product_applied_to_correct_part_of_door(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'The product must be applied to a door bottom seal or a set' \
            ' of door jamb and head seals or a combination of both, as' \
            ' prescribed in Implementation Requirement 1.'

    def formula(buildings, period, parameters):
        door_bottom_seal = buildings('product_applied_to_door_bottom_seal', period)
        set_door_jamb = buildings('product_applied_to_set_door_jamb', period)
        head_seals = buildings('product_applied_to_head_seals', period)
        return door_bottom_seal + (set_door_jamb * head_seals)


class product_restricts_airflow(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product effectively restricts airflow into or' \
            ' out of the site around the perimeter of the Door, as required' \
            ' in Implementation Requirement 2.'


class product_installed_according_to_instructions(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product has been installed in strict accordance' \
            ' with the manufacturer instructions, as prescribed by' \
            ' Implementation Requirement 3.'


class all_external_doors_are_draught_proofed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether all doors on the Site that meet the Eligibility' \
            ' Requirements, excluding sliding doors have been draught proofed,' \
            ' in accordance with Implementation Requirement 4.'  # this means you need to run the eligibility requirement for every door on the size and probably have a flag saying
