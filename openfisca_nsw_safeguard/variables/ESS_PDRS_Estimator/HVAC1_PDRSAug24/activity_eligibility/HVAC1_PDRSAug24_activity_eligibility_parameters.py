import numpy as np
from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building


class HVAC1_PDRSAug24_NewInstallationReplacement(Enum):
    new_installation_activity = 'Installation of a new air conditioner'
    replacement_activity = 'Replacement of an existing air conditioner'



class HVAC1_PDRSAug24_new_installation_or_replacement(BaseVariable):
    value_type = Enum
    entity = Building
    possible_values = HVAC1_PDRSAug24_NewInstallationReplacement
    default_value = HVAC1_PDRSAug24_NewInstallationReplacement.replacement_activity
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'display_question' : 'Which one of the following activities are you implementing?',
        'sorting' : 1
    }


class HVAC1_PDRSAug24_new_installation_or_replacement_eligible(BaseVariable):
    """Checks if the type of activity is eligible
    """
    value_type = bool
    entity = Building 
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      activity_type = buildings('HVAC1_PDRSAug24_new_installation_or_replacement', period)

      activity_type_eligible = np.select(
        [
          (activity_type == HVAC1_PDRSAug24_NewInstallationReplacement.new_installation_activity),
          (activity_type == HVAC1_PDRSAug24_NewInstallationReplacement.replacement_activity)
        ],
        [
          True,
          True
        ])

      return activity_type_eligible


class HVAC1_PDRSAug24_installed_by_qualified_person(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the removal of the existing equipment and the installation of the End-User equipment be performed or supervised by a suitably qualified licensed person?',
        'sorting' : 2,
        'eligibility_clause' : """In PDRS HVAC1 Implementation Requirements Clause 3 it states that the activity, including the removal of any existing End-User Equipment, must be performed or supervised by a suitably qualified licence holder in compliance with the relevant standards and legislation."""
    }


class HVAC1_PDRSAug24_equipment_installed(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the End-User equipment be installed accordance with AS/NZS 5141: 2018?',
        'sorting' : 3,
        'eligibility_clause' : """In PDRS HVAC1 Implementation Requirements Clause 2 it states that the New End-User Equipment or replacement End-User Equipment must be designed and installed in accordance with AS/NZS 5141: 2018"""
    }


class HVAC1_PDRSAug24_engaged_ACP(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 4,
        'eligibility_clause' : """In ESS Clause 6.2 it states that an Accredited Certificate Provider may only create Energy Savings Certificates in respect of the Energy Savings for an Implementation where:<br />
                                  (a) the Accredited Certificate Provider is the Energy Saver for those Energy Savings as at the Implementation Date; and <br />
                                  (b) the Accredited Certificate Provider’s Accreditation Date for that Recognised Energy Saving Activity is prior to the Implementation Date."""
    }


class HVAC1_PDRSAug24_minimum_payment(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Are you aware that you are required to make a minimum payment towards the cost of your upgrade?',
      'sorting' : 5,
      'eligibility_clause' : """In ESS Clause 9.8.1(f) it states that the Accredited Certificate Provider has evidence satisfactory to the Scheme Administrator that the Purchaser has paid for the Implementation, assessment and other associated works carried out at the Site a Net Amount (excluding GST) as set out in Table 1. Table 1 - Purchaser payments for Implementations under clause 9.8.1(f)<br />
                                (ii) at least $500 for an Implementation of Air Conditioners (other than Multi-split or Ducted systems) using Activity Definition D16;<br />
                                (iii) at least $1000 for Multi-split or Ducted systems up to 15 kW of cooling capacity using Activity Definition D16;<br />
                                (iv) at least $2000 for Multi-split or Ducted systems between 15 and 19 kW of cooling capacity using Activity Definition D16;<br />
                                (v) at least $3000 for Multi-split or Ducted systems greater than or equal to 20 kW of cooling capacity using Activity Definition D16."""
    }


class HVAC1_PDRSAug24_equipment_registered_in_GEMS(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the new air conditioner be recorded in the GEMS registry (as defined within the GEMS Determination 2019)?',
        'sorting' : 6,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 1 it states that the New End-User Equipment or replacement End-User Equipment must be registered as an air-to-air Air Conditioner in the GEMS Registry as complying with the Greenhouse and Energy Minimum Standards (Air Conditioners up to 65kW) Determination 2019 under Product Classes 5-12 or 18-21 as listed in the GEMS Registry."""
    }


class HVAC1_PDRSAug24_model_number_registered_in_GEMS(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the model number(s) match the model number(s) recorded in the GEMS registry?',
        'sorting' : 7,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 5 it states that if the New End-User Equipment or replacement End-User Equipment is an eligible system for Product Classes 5-12, the model number(s) must match the model number(s) recorded in the GEMS registry."""
    }


class HVAC1_PDRSAug24_multi_split_product_class(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the end user equipment be an outdoor Multi-split?',
        'sorting' : 8,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 6 it states that if the New End-User Equipment or replacement End-User Equipment is an eligible outdoor Multi-split system Product Type under the GEMS Registry for Product Classes 18-21."""
    }


class HVAC1_PDRSAug24_outdoor_units(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will all indoor and outdoor units use the same manufacturer brand?',
        'sorting' : 9,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 6(b) it states that if the manufacturer brand must be the same for all indoor and outdoor End-User Equipment, and"""
    }


class HVAC1_PDRSAug24_manufacture_approved_GEMS(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the system be a manufacturer approved combination with the outdoor unit matching the GEMS-registered model?',
        'sorting' : 10,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 6(a) it states that the outdoor unit part of the GEMS registered model number must match the model number of the outdoor unit being installed,<br />
                                  In PDRS HVAC1 Equipment Requirements Clause 6(c) it states that the unit(s) must be an approved combination by the manufacturer."""
    }


class HVAC1_PDRSAug24_new_equipment_cooling_capacity(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Will the new air conditioner have a cooling capacity recorded in the GEMS registry?',
        'sorting' : 11,
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 2 it states that if the New End-User Equipment or replacement End-User Equipment has a Cooling Capacity recorded in the GEMS Registry:"""
    }


class HVAC1_PDRSAug24_AEER_greater_than_minimum(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will your AEER equal to or greater than the Minimum AEER for the same Product Class and Cooling Capacity in ESS Table D16.4',
        'sorting' : 12,
        'conditional' : 'True',
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 2(b) it states that if it does not have a Residential TCSPF_mixed value recorded in the GEMS Registry, then it must have a Rated AEER in the GEMS Registry equal to or greater than the Minimum AEER for the same Product Class in Table D16.4."""
    }


class HVAC1_PDRSAug24_TCPSF_greater_than_minimum(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will your GEMS Residential TCSPF_mixed value equal to or greater than the Minimum Residential TCSPF_mixed value for the same Product Class and Cooling Capacity in ESS Table D16.4?',
        'sorting' : 13,
        'conditional' : 'True',
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 2(a) it states that it must have a Residential TCSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential TCSPF_mixed value for the same Product Class in Table D16.4; or """
    }


class DefaultValuesClimateZone(Enum):
    hot_zone = "Hot zone"
    average_zone = "Average zone"
    cold_zone = "Cold zone"


class HVAC1_PDRSAug24_climate_zone(BaseVariable): ### up to here #####
    value_type = Enum
    entity = Building
    possible_values = DefaultValuesClimateZone
    default_value = DefaultValuesClimateZone.average_zone
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Which climate zone is the End-User equipment installed in, as defined in ESS Table A27?',
        'sorting' : 9
    }


class HVAC1_PDRSAug24_new_equipment_heating_capacity(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Does the new or replacement End-User equipment have a heating capacity recorded in the GEMS Registry?'
    metadata = {
        'display_question' : 'Does the new or replacement End-User equipment have a heating capacity recorded in the GEMS Registry?',
        'sorting' : 10,
        'eligibility_clause' : """In ESS D16 Equipment Requirements Clauses 3 and 4 it states that:<br />
        3. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry, and is installed in the hot or average zone as defined in Table A27: <br />
          a. It must have a Residential HSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential HSPF_mixed value for the same Product Type and Cooling Capacity in Table D16.4; or<br />
          b. If it does not have a Residential HSPF_mixed value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table D16.5.<br />
        4. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry and is installed in the cold zone as defined in Table A27:<br />
          a. It must have a Residential HSPF_cold value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential HSPF_cold value for the same Product Type and Cooling Capacity in Table D16.4; or<br />
          b. If it does not have a Residential HSPF_cold value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table D16.5.
        """
    }


class HVAC1_PDRSAug24_HSPF_mixed_eligible(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is your GEMS Residential HSPF_mixed value equal to or greater than the Minimum Residential HSPF_mixed value for the same Product Type and Cooling Capacity in ESS Table D16.4?'
    metadata = {
        'display_question' : 'Is your GEMS Residential HSPF_mixed value equal to or greater than the Minimum Residential HSPF_mixed value for the same Product Type and Cooling Capacity in ESS Table D16.4?',
        'sorting' : 11,
        'conditional': 'True',
        'eligibility_clause' : """In ESS D16 Equipment Requirements Clauses 3 and 4 it states that:<br />
        3. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry, and is installed in the hot or average zone as defined in Table A27: <br />
        a. It must have a Residential HSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential HSPF_mixed value for the same Product Type and Cooling Capacity in Table D16.4; or<br />
        b. If it does not have a Residential HSPF_mixed value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table D16.5.<br />
        4. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry and is installed in the cold zone as defined in Table A27:<br />
        a. It must have a Residential HSPF_cold value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential HSPF_cold value for the same Product Type and Cooling Capacity in Table D16.4; or<br />
        b. If it does not have a Residential HSPF_cold value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table D16.5.
        """
    }


class HVAC1_PDRSAug24_ACOP_eligible(BaseVariable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    default_value = True
    label = 'Is your ACOP equal to or greater than the Minimum ACOP for the same Product Type and Cooling Capacity in ESS Table D16.5?'
    metadata = {
        'display_question' : 'Is your ACOP equal to or greater than the Minimum ACOP for the same Product Type and Cooling Capacity in ESS Table D16.5?',
        'sorting' : 12,
        'conditional': 'True',
        'eligibility_clause' : """In ESS D16 Equipment Requirements Clauses 3 and 4 it states that:<br />
        3. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry, and is installed in the hot or average zone as defined in Table A27: <br />
        a. It must have a Residential HSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential HSPF_mixed value for the same Product Type and Cooling Capacity in Table D16.4; or<br />
        b. If it does not have a Residential HSPF_mixed value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table D16.5.<br />
        4. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry and is installed in the cold zone as defined in Table A27:<br />
        a. It must have a Residential HSPF_cold value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential HSPF_cold value for the same Product Type and Cooling Capacity in Table D16.4; or<br />
        b. If it does not have a Residential HSPF_cold value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table D16.5.
        """
    }


class HVAC1_PDRSAug24_HSPF_cold_eligible(BaseVariable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is your GEMS Residential HSPF_cold value equal to or greater than the Minimum Residential HSPF_cold value for the same Product Type and Cooling Capacity in ESS Table D16.4?'
    metadata = {
        'display_question' : 'Is your GEMS Residential HSPF_cold value equal to or greater than the Minimum Residential HSPF_cold value for the same Product Type and Cooling Capacity in ESS Table D16.4?',
        'sorting' : 13,
        'conditional': 'True',
        'eligibility_clause' : """In ESS D16 Equipment Requirements Clauses 3 and 4 it states that:<br />
        3. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry, and is installed in the hot or average zone as defined in Table A27: <br />
        a. It must have a Residential HSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential HSPF_mixed value for the same Product Type and Cooling Capacity in Table D16.4; or<br />
        b. If it does not have a Residential HSPF_mixed value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table D16.5.<br />
        4. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry and is installed in the cold zone as defined in Table A27:<br />
        a. It must have a Residential HSPF_cold value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential HSPF_cold value for the same Product Type and Cooling Capacity in Table D16.4; or<br />
        b. If it does not have a Residential HSPF_cold value recorded in the GEMS Registry, then it must have a Rated ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling Capacity in Table D16.5.
        """
    }