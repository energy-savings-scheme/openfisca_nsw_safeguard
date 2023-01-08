from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class RF2_equipment_replaced(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the replacement of an existing refrigerated cabinet?',
      'sorting' : 1,
      'conditional' : 'True',
      'eligibility_clause' : """In PDRS RF2 Eligibility Requirements Clause 1 is states that this activity must be a replacement of an existing Refrigerated Cabinet (whether operational or not) with a high efficiency Refrigerated Cabinet."""
    }


class RF2_installation(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the installation of a new refrigerated cabinet?',
      'sorting' : 2,
      'eligibility_clause' : """This activity is only eligible for ESCs, in PDRS RF2 Eligibility Requirements Clause 1 is states that this activity must be a replacement of an existing Refrigerated Cabinet (whether operational or not) with a high efficiency Refrigerated Cabinet."""
    }


class RF2_qualified_install_removal(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Has the removal of the existing equipment and the installation of the end-user equipment been performed or supervised by a suitably licensed person?',
      'sorting' : 3,
      'eligibility_clause' : """In PDRS RF2 Implementation Requirements Clause 3 it states that the activity, including the removal of the existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class RF2_legal_disposal(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Has the existing End-User equipment been removed and disposed of in accordance with legislation?',
      'sorting' : 4,
      'eligibility_clause' : """In PDRS RF2 Implementation Requirements Clause 1 it states that the existing End-User Equipment must be removed and disposed of in accordance with legislation."""
    }


class RF2_equipment_installed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is the new End-User equipment installed and operational?'
    metadata = {
        'display_question' : 'Is the new End-User equipment installed and operational?',
        'sorting' : 5,
        'eligibility_clause' : """In PDRS RF2 Implementation Requirements Clause 2 it states that the replacement End-User Equipment must be installed in its intended place of use and operating."""
    }


class RF2_equipment_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the installed End-User equipment a registered product on the GEMS registry under GEMS (refrigerated cabinets) Determination 2020?',
        'sorting' : 6,
        'eligibility_clause' : """In PDRS RF2 Equipment Requirements Clause 1 it states that the End-User Equipment must be a Refrigerated Cabinet (RC) as defined within the terms of the Greenhouse and Energy Minimum Standards (Refrigerated Cabinets) Determination 2020."""
    }


class RF2_GEMS_product_class_5(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User equipment GEMS Product Class 5?',
      'sorting' : 7,
      'conditional' : 'True',
      'eligibility_clause' : """In PDRS RF2 Equipment Requirements Clause 2 it states that the refrigerated cabinet must have an Energy Efficiency Index (EEI) below 81, as recorded in the GEMS Registry, with the exception of Integral Ice Cream Freezer Cabinets (class 5) which must have an EEI below 51, as recorded in the GEMS Registry."""
    }


class RF2_EEI_under_51(Variable):
    #if the equipment is Product Class 5, the EEI must be below 51 to be eligible
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the product Energy Efficiency Index (EEI) as recorded in the GEMS Registry below 51?',
      'sorting' : 8,
      'eligibility_clause' : """In PDRS RF2 Equipment Requirements Clause 2 it states that the refrigerated cabinet must have an Energy Efficiency Index (EEI) below 81, as recorded in the GEMS Registry, with the exception of Integral Ice Cream Freezer Cabinets (class 5) which must have an EEI below 51, as recorded in the GEMS Registry."""
    }


class RF2_EEI_under_81(Variable):
    #if the equipment is anything other than Product Class 5, the EEI must be below 81 to be eligible
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the product Energy Efficiency Index (EEI) as recorded in the GEMS Registry below 81?',
      'sorting' : 9,
      'eligibility_clause' : """In PDRS RF2 Equipment Requirements Clause 2 it states that the refrigerated cabinet must have an Energy Efficiency Index (EEI) below 81, as recorded in the GEMS Registry, with the exception of Integral Ice Cream Freezer Cabinets (class 5) which must have an EEI below 51, as recorded in the GEMS Registry."""
    }