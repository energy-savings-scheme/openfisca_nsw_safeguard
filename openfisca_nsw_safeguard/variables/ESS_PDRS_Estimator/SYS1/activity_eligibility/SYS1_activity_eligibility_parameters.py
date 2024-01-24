from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class SYS1_new_motor_for_ventilation_refrigeration(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the installation of a new motor for a ventilation or refrigeration application?',
      'sorting' : 1,
      'eligibility_clause' : """In PDRS SYS1 Eligibility Requirements Clause 1 it states that the motor must be installed for use in ventilation or refrigeration applications."""
    }


class SYS1_equipment_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the new End-User equipment a registered product on the GEMS registry under GEMS (Three Phase Cage Induction Motors) Determination 2019?',
        'sorting' : 2,
        'eligibility_clause' : """In PDRS SYS1 Equipment Requirements Clause 2 it states that The electric motor must be a registered product under GEMS and comply with the Greenhouse and Energy Minimum Standards (Three Phase Cage Induction Motors) Determination 2019."""
    }


class SYS1_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 3,
        'eligibility_clause' : """In ESS Clause 6.2 it states that an Accredited Certificate Provider may only create Energy Savings Certificates in respect of the Energy Savings for an Implementation where:<br />
                                  (a) the Accredited Certificate Provider is the Energy Saver for those Energy Savings as at the Implementation Date; and <br />
                                  (b) the Accredited Certificate Provider’s Accreditation Date for that Recognised Energy Saving Activity is prior to the Implementation Date."""
    }


class SYS1_high_efficiency(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the new End-User equipment a 3-phase, high efficiency electric motor?',
      'sorting' : 4,
      'eligibility_clause' : """In PDRS SYS1 Equipment Requirements Clause 1 it states that the End-User Equipment must be a 3 phase electric motor rated high efficiency within the meaning of Part 5 of the Greenhouse and Energy Minimum Standards (Three Phase Cage Induction Motors) Determination 2019 when tested in accordance with subclause 6.1.3 of IEC60034-2-1."""
    }   


class SYS1_equipment_installed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Has the new End-User equipment been installed?',
      'sorting' : 5,
      'eligibility_clause' : """In PDRS SYS1 Implementation Requirements Clause 1 it states that the electric motor must be installed."""
    }


class SYS1_rated_output_eligible(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the electric motors rated output between 0.73kW and 185kW?',
      'sorting' : 6,
      'eligibility_clause' : """The electric motor must have a rated output from 0.73kW to <185kW."""
    }