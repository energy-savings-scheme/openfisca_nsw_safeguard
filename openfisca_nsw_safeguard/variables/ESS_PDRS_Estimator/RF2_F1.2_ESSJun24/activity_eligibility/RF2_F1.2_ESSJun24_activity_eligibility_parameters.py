from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building
import numpy as np


class RF2_F1_2_ESSJun24_equipment_replaced(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the replacement of an existing refrigerated cabinet?',
      'sorting' : 1,
      'eligibility_clause' : """In PDRS RF2 Eligibility Requirements Clause 1 it states that this activity must be a replacement of an existing Refrigerated Cabinet (whether operational or not) with a high efficiency Refrigerated Cabinet."""
    }


class RF2_F1_2_ESSJun24_same_product_class(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {  
      'display_question' : 'Is the new End-User equipment the same product class as the old refrigerated display cabinet?',
      'sorting' : 2,
      'eligibility_clause' : """ In ESS F1.2 Equipment Requirements Clause 5 it states that the existing End-User Equipment (that is, the End-User Equipment that is replaced as part of the Implementation) must be either: <br />
                                a) recorded on the GEMS Registry as being either or both of: <br />
                                i) the same Refrigerated Cabinet Product Class as the replacement End-User Equipment, as set out in the second column of Table F1.2.1; or <br />
                                ii) an AS 1731.14 Product Type, as set out in the third column of Table F1.2.1, that is in the same row of Table F1.2.1 as the Refrigerated Cabinet Product Class of the replacement End-User-Equipment, as set out in the second column of Table F1.2.1; or<br />
                                b) in fact of an AS 1731.14 Product Type, as set out in the third column of Table F1.2.1, that is in the same row of Table F1.2.1 as the Refrigerated Cabinet Product Class of the replacement End-User-Equipment, as set out in the second column of Table F1.2.1, with that fact to be evidenced to the satisfaction of the Scheme Administrator."""
    } 

class RF2_F1_2_ESSJun24_qualified_install_removal(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Will the removal of the existing equipment and the installation of the End-User equipment be performed or supervised by a suitably licensed person?',
      'sorting' : 3,
      'eligibility_clause' : """In ESS F1.2 and PDRS RF2 Implementation Requirements Clause 3 it states that the activity, including the removal of the existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class RF2_F1_2_ESSJun24_legal_disposal(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Will the existing End-User equipment be removed and disposed of in accordance with legislation?',
      'sorting' : 4,
      'eligibility_clause' : """In ESS F1.2 and PDRS RF2 Implementation Requirements Clause 1 it states that the existing End-User Equipment must be removed and disposed of in accordance with legislation."""
    }


class RF2_F1_2_ESSJun24_engaged_ACP(BaseVariable):
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


class RF2_F1_2_ESSJun24_minimum_payment(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Are you aware that you are required to make a minimum payment towards the cost of your upgrade?',
      'sorting' : 6,
      'eligibility_clause' : """In ESS Clause 9.9.1E it states that the Accredited Certificate Provider has evidence satisfactory to the Scheme Administrator that the Purchaser has paid for the Implementation, assessment and other associated works carried out at the Site a Net Amount of at least $1000 (excluding GST) for each item of End-User Equipment installed as part of an Implementation using any of Activity Definitions F1.1, F1.2, F16 or F17."""
    }


class RF2_F1_2_ESSJun24_installed_on_site(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the new End-User equipment operating in its intended place of use?',
      'sorting' : 7,
      'eligibility_clause' : """In ESS F1.1, ESS F1.2 and and PDRS RF2 Implementation Requirements Clause 2 is states that the replacement End-User Equipment must be installed in its intended place of use and operating."""
    }


class RF2_F1_2_ESSJun24_display_sides(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the new End-User equipment have only one display side?',
        'sorting' : 8,
        'eligibility_clause' : """In ESS F1.1, ESS F1.2 and PDRS RF2 Equipment Requirements Clause 4 it states that the new End-User Equipment must not have 2 or more display sides."""
    }


class RF2_F1_2_ESSJun24_equipment_registered_in_GEMS(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the new End-User equipment a registered product on the GEMS registry under GEMS (refrigerated cabinets) Determination 2024?',
        'sorting' : 9,
        'eligibility_clause' : """In ESS F1.1, ESS F1.2 and PDRS RF2 Equipment Requirements Clause 1 it states that the End-User Equipment must be a Refrigerated Cabinet (RC) as defined within the terms of the Greenhouse and Energy Minimum Standards (Refrigerated Cabinets) Determination 2024."""
    }


class RF2_F1_2_ESSJun24_GEMS_product_class_12(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the GEMS Product Class of the new End-User equipment 12 or above?',
      'sorting' : 10,
      'conditional' : 'True',
      'eligibility_clause' : """In ESS clauses 6.12A and 6.12B and PDRS clause 6.9.2B it states that an activity that involves the installation of End-User Equipment that is of Refrigerated Cabinet Product Classes 1-11 is suspended."""
    }


class RF2_F1_2_ESSJun24_EEI_under_77(BaseVariable):
    #if Q1 is New Installation
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the Energy Efficiency Index (EEI) of the new End-User equipment below 77, as recorded in the GEMS Registry?',
      'sorting' : 11,
      'eligibility_clause' : """In ESS F1.1 Equipment Requirements Clause 2 it states that the refrigerated cabinet must have an Energy Efficiency Index (EEI) below 77, as recorded in the GEMS Registry."""
    }


class RF2_F1_2_ESSJun24_EEI_under_81(BaseVariable):
    #if Q1 is Replacement 
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the Energy Efficiency Index (EEI) of the new End-User equipment below 81, as recorded in the GEMS Registry?',
      'sorting' : 12,
      'eligibility_clause' : """In ESS F1.2 and PDRS RF2 Equipment Requirements Clause 2 it states that the refrigerated cabinet must have an Energy Efficiency Index (EEI) below 81, as recorded in the GEMS Registry."""
    }