import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class D17_equipment_replaced(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the replacement of an existing electric water heater with an (air source) heat pump water heater?',
      'sorting' : 1,
      'eligibility_clause' : """A new installation is not eligible under ESS Activity D17. In ESS D17 the activity definition states that the activity must be the replacement of an existing electric water heater with an (air source) heat pump water heater."""
    }


class D17_equipment_replaces_electric(Variable):
    #replacement of an existing gas hot water heater or boiler is a different activity under the ESS (D19)
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the equipment being replaced an electric resistance storage or instantaneous water heater?',
      'sorting' : 2,
      'eligibility_clause' : """In ESS D17 Eligibility Requirements Clause 1 it states that the existing electric water heater must be an electric resistance storage or instantaneous water heater."""
    }


class D17_engaged_ACP(Variable):
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


class D17_equipment_removed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the existing equipment been removed',
        'sorting' : 4,
        'eligibility_clause' : """In ESS D17 Implementation Requirements Clause 1 it states that the existing End-User Equipment must be removed."""
    }


class D17_equipment_installed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the replacement equipment been installed?',
        'sorting' : 5,
        'eligibility_clause' : """In ESS D17 Implementation Requirements Clause 2 it states that the replacement End-User Equipment must be installed at a Site in accordance with the Equipment Requirements."""
    }


class D17_installed_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the removal of the existing equipment and the installation of the End-User equipment been performed or supervised by a suitably licensed person?',
        'sorting' : 6,
        'eligibility_clause' : """In ESS D17 Implementation Requirements Clause 3, it states that the activity, including the removal of any existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class D17_equipment_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the installed air source heat pump a registered product on the GEMS Registry?',
        'sorting' : 7,
        'eligibility_clause' : """In order to meet GEMS certification, the product must meet two requirements required by this activity:<br /> 
                                  1.The installed End-User Equipment must be an air source heat pump water heater as defined by AS/NZS 4234; and <br />
                                  2. The installed End-User Equipment must be certified to AS/NZS 2712."""
    }