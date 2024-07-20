from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np



class SYS2_PDRSAug24_NewInstallationReplacement(Enum):
    new_installation_activity = 'Installation of a new pool pump'
    replacement_activity = 'Replacement of an existing pool pump'



class SYS2_PDRSAug24_new_installation_or_replacement(Variable):
    value_type = Enum
    entity = Building
    possible_values = SYS2_PDRSAug24_NewInstallationReplacement
    default_value = SYS2_PDRSAug24_NewInstallationReplacement.replacement_activity
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'display_question' : 'Which one of the following activities are you implementing?',
        'sorting' : 1,
        'eligibility_clause' : """The SYS2 activity is defined as the replacement of an existing pool pump with a high-efficiency pool pump."""
    }


class SYS2_PDRSAug24_new_installation_or_replacement_eligible(Variable):
    """Checks if the type of activity is eligible
    """
    value_type = bool
    entity = Building 
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      activity_type = buildings('SYS2_PDRSAug24_new_installation_or_replacement', period)

      activity_type_eligible = np.select(
        [
          (activity_type == SYS2_PDRSAug24_NewInstallationReplacement.new_installation_activity),
          (activity_type == SYS2_PDRSAug24_NewInstallationReplacement.replacement_activity)
        ],
        [
          False,
          True
        ])

      return activity_type_eligible


class SYS2_PDRSAug24_existing_equipment_removed(Variable):
    #only show this question if the activity is a replacement
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the existing End-User equipment been removed?',
        'sorting' : 2,
        'conditional' : 'True',
        'eligibility_clause' : """In ESS D5 Implementation Requirements Clause 1 it states that if there is any existing End-User Equipment, it must be removed."""
    }


class SYS2_PDRSAug24_replacement_existing_equipment_removed(Variable):
    """Checks if it's a replacement, and if it is, that the existing equipment has been removed  
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    
    def formula(buildings, period, parameters):
      activity_type = buildings('SYS2_PDRSAug24_new_installation_or_replacement', period)
      existing_equipment_removed = buildings('SYS2_PDRSAug24_existing_equipment_removed', period)

      activity_type_existing_equipment_removed = np.select(
        [
          (activity_type == SYS2_PDRSAug24_NewInstallationReplacement.new_installation_activity) * existing_equipment_removed,
          (activity_type == SYS2_PDRSAug24_NewInstallationReplacement.new_installation_activity) * np.logical_not(existing_equipment_removed),
          (activity_type == SYS2_PDRSAug24_NewInstallationReplacement.replacement_activity) * existing_equipment_removed,
          (activity_type == SYS2_PDRSAug24_NewInstallationReplacement.replacement_activity) * np.logical_not(existing_equipment_removed)
        ],
        [
          True,
          False,
          False,
          False
        ])

      return activity_type_existing_equipment_removed


class SYS2_PDRSAug24_equipment_installed_on_site(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the new or replacement pool pump been installed on Site?',
        'sorting' : 3,
        'eligibility_clause' : """In ESS D5 Implementation Requirements Clause 2 it states that the new or replacement End-User Equipment must be installed."""
    }


class SYS2_PDRSAug24_qualified_install_removal(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Will the removal of the existing equipment and the installation of the End-User equipment be performed or supervised by a suitably licensed person?',
      'sorting' : 4,
      'eligibility_clause' : """In ESS D5 Implementation Requirements Clause 3 it states that the activity, including the removal of the existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class SYS2_PDRSAug24_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 5,
        'eligibility_clause' : """In ESS Clause 6.2 it states that an Accredited Certificate Provider may only create Energy Savings Certificates in respect of the Energy Savings for an Implementation where:<br />
                                  (a) the Accredited Certificate Provider is the Energy Saver for those Energy Savings as at the Implementation Date; and <br />
                                  (b) the Accredited Certificate Provider’s Accreditation Date for that Recognised Energy Saving Activity is prior to the Implementation Date."""
    }


class SYS2_PDRSAug24_minimum_payment(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Are you aware that you are required to make a minimum payment towards the cost of your upgrade?',
      'sorting' : 6,
      'eligibility_clause' : """In ESS Clause 9.8.1E it states that the Accredited Certificate Provider has evidence satisfactory to the Scheme Administrator that the Purchaser has paid for the Implementation, assessment and other associated works carried out at the Site a Net Amount of at least $200 (excluding GST) for each item of End-User Equipment installed as part of an Implementation using any of Activity Definitions F1.1, F1.2, F16 or F17."""
    }


class SYS2_PDRSAug24_equipment_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the installed End-User equipment a registered product on the GEMS registry under GEMS (Swimming Pool Pump-units) Determination 2021?',
        'sorting' : 7,
        'eligibility_clause' : """In ESS D5 Equipment Requirements Clause 1 it states that the new End-User Equipment must be listed as part of a labelling scheme determined in accordance with the Equipment Energy Efficiency (E3) Committee's Voluntary Energy Rating Labelling Program for Swimming Pool Pump-units: Rules for Participation, April 2010, or be a registered product in the GEMS Registry as complying with the Greenhouse and Energy Minimum Standards (Swimming Pool Pump-units) Determination 2021."""
    }


class SYS2_PDRSAug24_star_rating_minimum_four(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Does the new End-User equipment have a minimum star rating of 4?',
      'sorting' : 8,
      'eligibility_clause' : """In ESS D5 Equipment Requirements Clause 2 it states that the new or replacement End-User Equipment must have a star rating, as recorded in the GEMS Registry, equal to or greater than 4."""
    }


class SYS2_PDRSAug24_warranty(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Does the new End-User equipment have a warranty of at least 3 years?',
      'sorting' : 9,
      'eligibility_clause' : """In ESS D5 Equipment Requirements Clause 3 it states that the new End-User Equipment must have a warranty of at least 3 years."""
    }
