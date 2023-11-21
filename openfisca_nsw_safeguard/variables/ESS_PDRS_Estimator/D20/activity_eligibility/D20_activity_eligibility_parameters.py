import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class D20_equipment_replaced(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the replacement of an existing gas water heater with a solar (electric boosted) water heater?',
      'sorting' : 1,
      'eligibility_clause' : """A new installation is not eligible under ESS Activity D20. In ESS D20 the activity definition states that the activity must be the replacement of an existing gas water heater with a solar (electric boosted) water heater."""
    }


class D20_equipment_replaces_gas(Variable):
    #replacement of an existing electric hot water heater with a solar heater is a different activity under the ESS (D18)
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the equipment being replaced a gas storage or instantaneous water heater',
      'sorting' : 2,
      'eligibility_clause' : """In ESS D20 Eligibility Requirements Clause 1 it states that the existing gas water heater must be a gas storage or instantaneous water heater."""
    }


class D20_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Was or will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 3,
        'eligibility_clause' : """In ESS Clause 6.2 it states that an Accredited Certificate Provider may only create Energy Savings Certificates in respect of the Energy Savings for an Implementation where:<br />
                                  (a) the Accredited Certificate Provider is the Energy Saver for those Energy Savings as at the Implementation Date; and <br />
                                  (b) the Accredited Certificate Provider’s Accreditation Date for that Recognised Energy Saving Activity is prior to the Implementation Date."""
    }


class D20_equipment_removed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the existing equipment been removed?',
        'sorting' : 4,
        'eligibility_clause' : """In ESS D20 Implementation Requirements Clause 1 it states that the existing End-User Equipment must be removed."""
    }


class D20_equipment_installed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the replacement equipment been installed?',
        'sorting' : 5,
        'eligibility_clause' : """In ESS D20 Implementation Requirements Clause 2 it states that the replacement End-User Equipment must be installed at a Site in accordance with the Equipment Requirements."""
    }


class D20_installed_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the removal of the existing equipment and the installation of the End-User equipment been performed or supervised by a suitably licensed person?',
        'sorting' : 6,
        'eligibility_clause' : """In ESS D20 Implementation Requirements Clause 3, it states that the activity, including the removal of any existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class D20_equipment_registered_IPART(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the installed air source heat pump a registered product on the IPART Registry?',
        'sorting' : 7,
        'eligibility_clause' : """In order to be listed on the IPART product registry, the product has met the following three product requirements of this activity:<br /> 
                                  1. The installed End-User Equipment must be a solar water heater with a collector as defined in AS/NZS 4234;<br />
                                  2. The installed End-User Equipment must be certified to AS/NZS 2712; and <br />
                                  3. The installed End-User Equipment must achieve minimum annual energy savings of 60% when determined as a solar thermal collector system with supplementary electric resistive heating in AS/NZS 4234 climate zone 3 using a small or medium thermal peak load in accordance with AS/NZS 4234, for all Sites in an ESS Jurisdiction."""
    }