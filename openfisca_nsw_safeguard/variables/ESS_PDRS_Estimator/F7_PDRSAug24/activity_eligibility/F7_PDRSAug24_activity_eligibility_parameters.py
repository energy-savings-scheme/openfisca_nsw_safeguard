from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class F7_PDRSAug24_high_efficiency(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the new End-User equipment a 3-phase, high efficiency electric motor?',
        'sorting' : 1,
        'eligibility_clause' : """In ESS F7 Equipment Requirements Clause 1 it states that the End-User Equipment must be a 3 phase electric motor rated high efficiency within the meaning of Part 5 of the Greenhouse and Energy Minimum Standards (Three Phase Cage Induction Motors) Determination 2019 when tested in accordance with subclause 6.1.3 of IEC60034-2-1."""
    }   


class F7_PDRSAug24_equipment_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the new End-User equipment a registered product on the GEMS registry under GEMS (Three Phase Cage Induction Motors) Determination 2019?',
        'sorting' : 2,
        'eligibility_clause' : """In ESS F7 Equipment Requirements Clause 2 it states that the electric motor must be a registered product under GEMS and comply with the Greenhouse and Energy Minimum Standards (Three Phase Cage Induction Motors) Determination 2019."""
    }


class F7_PDRSAug24_equipment_installed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the new End-User equipment been installed?',
        'sorting' : 3,
        'eligibility_clause' : """In ESS F7 Implementation Requirements Clause 1 it states that the electric motor must be installed."""
    }


class F7_PDRSAug24_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Was an Accredited Certificate Provider engaged before the implementation date?',
        'sorting' : 4,
        'eligibility_clause' : """In ESS Clause 6.2 it states that an Accredited Certificate Provider may only create Energy Savings Certificates in respect of the Energy Savings for an Implementation where:<br />
                                  (a) the Accredited Certificate Provider is the Energy Saver for those Energy Savings as at the Implementation Date; and <br />
                                  (b) the Accredited Certificate Provider’s Accreditation Date for that Recognised Energy Saving Activity is prior to the Implementation Date."""
    }


class F7_PDRSAug24_rated_output_eligible(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the electric motor’s rated output between 0.73kW and 185kW?',
        'sorting' : 5,
        'eligibility_clause' : """In ESS F7 Implementation Requirements Clause 2 it states that the electric motor must have a rated output from 0.73kW to <185kW."""
    }