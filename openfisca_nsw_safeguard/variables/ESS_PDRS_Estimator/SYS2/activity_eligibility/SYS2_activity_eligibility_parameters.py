from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class SYS2_equipment_replaced(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the activity the replacement of an existing pool pump?',
        'sorting' : 1,
        'eligibility_clause' : """The SYS2 activity is defined as the replacement of an existing pool pump with a high-efficiency pool pump."""
    }


class SYS2_old_equipment_installed_on_site(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Was the existing pool pump installed on Site at time of replacement?',
        'sorting' : 2,
        'eligibility_clause' : """In PDRS SYS2 Eligibility Requirements Clause 1 it states that there must be an existing pool pump installed at the Site at time of replacement."""
    }


class SYS2_qualified_install_removal(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Has the removal of the existing equipment and the installation of the end-user equipment been performed or supervised by a suitably licensed person?',
      'sorting' : 3,
      'eligibility_clause' : """In PDRS SYS2 Implementation Requirements Clause 1 it states that the activity, including the removal of the existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class SYS2_legal_disposal(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Has the decommissioned pool pump been removed in accordance with relevant safety standards and legislation?',
      'sorting' : 4,
      'eligibility_clause' : """In PDRS SYS2 Implementation Requirements Clause 2 it states that the decommissioned pool pump must be removed in accordance with relevant safety standards and legislation."""
    }

    
class SYS2_equipment_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the installed End-User equipment a registered product on the GEMS registry under GEMS (Swimming Pool Pump-units) Determination 2021?',
        'sorting' : 5,
        'eligibility_clause' : """In PDRS SYS2 Equipment Requirements Clause 2 it states that the new End-User Equipment must be listed as part of a labelling scheme determined in accordance with the Equipment Energy Efficiency (E3) Committee's Voluntary Energy Rating Labelling Program for Swimming Pool Pump-units: Rules for Participation, April 2010, or be a registered product in the GEMS Registry as complying with the Greenhouse and Energy Minimum Standards (Swimming Pool Pump-units) Determination 2021."""
    }


class SYS2_voluntary_labelling_scheme(Variable):
    #only show this question if SYS2_equipment_registered_in_GEMS is false
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the installed End-User equipment listed as part of the Equipment Energy Efficiency (E3) Committees Voluntary Energy Rating Labelling Program for Swimming Pool Pump-units: Rules for Participation, April 2010?',
      'sorting' : 6,
      'conditional': 'True',
      'eligibility_clause' : """In PDRS SYS2 Equipment Requirements Clause 2 it states that the new End-User Equipment must be listed as part of a labelling scheme determined in accordance with the Equipment Energy Efficiency (E3) Committee's Voluntary Energy Rating Labelling Program for Swimming Pool Pump-units: Rules for Participation, April 2010, or be a registered product in the GEMS Registry as complying with the Greenhouse and Energy Minimum Standards (Swimming Pool Pump-units) Determination 2021."""
    }


class SYS2_star_rating_minimum_four_and_a_half(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Does the new End-User equipment have a minimum star rating of 4.5?',
      'sorting' : 7,
      'eligibility_clause' : """In PDRS SYS2 Equipment Requirements Clause 3 it states that the new End-User Equipment must achieve a minimum 4.5 star rating when determined in accordance with AS 5102.2."""
    }


class SYS2_warranty(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Does the new End-User equipment have a warranty of at least 3 years?',
      'sorting' : 8,
      'eligibility_clause' : """In PDRS SYS2 Equipment Requirements Clause 4 it states that the new End-User Equipment must have a warranty of at least 3 years."""
    }


class SYS2_single_phase(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the new End-User equipment single phase?',
      'sorting' : 9,
      'eligibility_clause' : """In PDRS SYS2 Equipment Requirements Clause 1 it states that the New End-User Equipment must be a product for use with a domestic pool or spa that is a single phase motor and any of the following types: single speed, two speed, multi speed or variable speed pump unit. The pump unit must have an input power of not less than 600W and not more than 1,700W for single speed pumps and 3,450W for two speed, multi speed and variable speed pumps when tested in accordance with AS 5102.1."""
    }


class SYS2_multiple_speed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the pool pump any of the following types: single speed, two speed, multi speed, variable speed?',
      'sorting' : 10,
      'eligibility_clause' : """In PDRS SYS2 Equipment Requirements Clause 1 it states that the New End-User Equipment must be a product for use with a domestic pool or spa that is a single phase motor and any of the following types: single speed, two speed, multi speed or variable speed pump unit. The pump unit must have an input power of not less than 600W and not more than 1,700W for single speed pumps and 3,450W for two speed, multi speed and variable speed pumps when tested in accordance with AS 5102.1."""
    }


class SYS2_multiple_speeds_input_power(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the input power of the pump unit between 600w and 3450w?',
      'sorting' : 11,
      'eligibility_clause' : """In PDRS SYS2 Equipment Requirements Clause 1 it states that the New End-User Equipment must be a product for use with a domestic pool or spa that is a single phase motor and any of the following types: single speed, two speed, multi speed or variable speed pump unit. The pump unit must have an input power of not less than 600W and not more than 1,700W for single speed pumps and 3,450W for two speed, multi speed and variable speed pumps when tested in accordance with AS 5102.1."""
    }


class SYS2_single_speed_input_power(Variable):
    #only display this question if SYS2_multiple_speed is false
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the input power of the pump unit between 600w and 1700w?',
      'sorting' : 12,
      'conditional': 'True',
      'eligibility_clause' : """In PDRS SYS2 Equipment Requirements Clause 1 it states that the New End-User Equipment must be a product for use with a domestic pool or spa that is a single phase motor and any of the following types: single speed, two speed, multi speed or variable speed pump unit. The pump unit must have an input power of not less than 600W and not more than 1,700W for single speed pumps and 3,450W for two speed, multi speed and variable speed pumps when tested in accordance with AS 5102.1."""
    }