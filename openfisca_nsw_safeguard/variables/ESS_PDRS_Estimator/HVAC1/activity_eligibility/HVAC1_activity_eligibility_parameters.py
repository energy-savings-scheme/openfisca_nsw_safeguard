import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class HVAC1_installation(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the activity the installation of a new air conditioner?',
        'sorting' : 1,
        'eligibility_clause' : """In PDRS HVAC1 Eligibility Requirements Clause 1, it states that this activity must be an installation of a new high efficiency air conditioner or a replacement of an existing air conditioner (whether operational or not) with a high efficiency air conditioner."""
    }


class HVAC1_equipment_replaced(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the activity the replacement of an existing air conditioner?',
        'sorting' : 2,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC1 Eligibility Requirements Clause 1, it states that this activity must be an installation of a new high efficiency air conditioner or a replacement of an existing air conditioner (whether operational or not) with a high efficiency air conditioner."""
    }


class HVAC1_installed_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the removal of the existing equipment and the installation of the end-user equipment been performed or supervised by a suitably licensed person?',
        'sorting' : 3,
        'eligibility_clause' : """In PDRS HVAC1 Implementation Requirements Clause 3, it states that the activity, including the removal of any existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class HVAC1_equipment_installed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the new End-User equipment installed and operational?',
        'sorting' : 4,
        'eligibility_clause' : """In PDRS HVAC1 Implementation Requirements Clause 2, it states that the New End-User Equipment or replacement End-User Equipment must be installed."""
    }


class HVAC1_equipment_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the new air conditioner recorded in the GEMS registry (as defined within the GEMS Determination 2019)?',
        'sorting' : 5,
        'conditonal' : 'True',
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 1 it states that the New End-User Equipment or replacement End-User Equipment must be a registered product in the GEMS Registry as complying with the Greenhouse and Energy Minimum Standards (Air Conditioners up to 65kW) Determination 2019.  """
    }


class HVAC1_new_equipment_cooling_capacity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Does the new air conditioner have a cooling capacity recorded in the GEMS registry?',
        'sorting' : 7,
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 2 it states that if the New End-User Equipment or replacement End-User Equipment has a Cooling Capacity recorded in the GEMS Registry: <br />
        a. The New End-User Equipment or replacement End-User Equipment must have a Residential TCSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential TCSPF_mixed value for the corresponding Product Type and Cooling Capacity in Table HVAC1.3; or <br />
        b. If the New End-User Equipment or replacement End-User Equipment does not have a Residential TCSPF_mixed value recorded in the GEMS Registry, then it must have an AEER in the GEMS Registry equal to or greater than the Minimum AEER for the Product Type and Cooling Capacity in Table HVAC1.4."""
    }


class HVAC1_AEER_greater_than_minimum(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is your AEER equal to or greater than the Minimum AEER for the Product Type and Cooling Capacity in PDRS Table HVAC1.4?',
        'sorting' : 7,
        'conditional' : 'True',
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 2 it states that if the New End-User Equipment or replacement End-User Equipment has a Cooling Capacity recorded in the GEMS Registry: <br />
        a. The New End-User Equipment or replacement End-User Equipment must have a Residential TCSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential TCSPF_mixed value for the corresponding Product Type and Cooling Capacity in Table HVAC1.3; or <br />
        b. If the New End-User Equipment or replacement End-User Equipment does not have a Residential TCSPF_mixed value recorded in the GEMS Registry, then it must have an AEER in the GEMS Registry equal to or greater than the Minimum AEER for the Product Type and Cooling Capacity in Table HVAC1.4."""
    }


class HVAC1_TCPSF_greater_than_minimum(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is your Residential TCSPF_mixed value equal to or greater than the Minimum Residential TCPSF_mixed value for the same Product Type and Cooling Capacity in PDRS Table HVAC1.3?',
        'sorting' : 8,
        'conditional' : 'True',
        'eligibility_clause' : """In PDRS HVAC1 Equipment Requirements Clause 2 it states that if the New End-User Equipment or replacement End-User Equipment has a Cooling Capacity recorded in the GEMS Registry: <br />
        a. The New End-User Equipment or replacement End-User Equipment must have a Residential TCSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the Minimum Residential TCSPF_mixed value for the corresponding Product Type and Cooling Capacity in Table HVAC1.3; or <br />
        b. If the New End-User Equipment or replacement End-User Equipment does not have a Residential TCSPF_mixed value recorded in the GEMS Registry, then it must have an AEER in the GEMS Registry equal to or greater than the Minimum AEER for the Product Type and Cooling Capacity in Table HVAC1.4."""
    }


class DefaultValuesClimateZone(Enum):
    hot_zone = "Hot zone"
    average_zone = "Average zone"
    cold_zone = "Cold zone"


class HVAC1_climate_zone(Variable):
    value_type = Enum
    entity = Building
    possible_values = DefaultValuesClimateZone
    default_value = DefaultValuesClimateZone.average_zone
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Which climate zone is the End-User equipment installed in, as defined in ESS Table A27?',
        'sorting' : 9
    }


class HVAC1_new_equipment_heating_capacity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Does the new or replacement End-User equipment have a heating capacity recorded in the GEMS Registry?'
    metadata = {
        'display_question' : 'Does the new or replacement End-User equipment have a heating capacity recorded in the GEMS Registry?',
        'sorting' : 11,
        'eligibility_clause' : """In ESS D16 Equipment Requirements Clauses 3 and 4 it states that:<br />
        3. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry,
        and is installed in the hot or average zone as defined in Table A27: <br />
        a. It must have a Residential HSPF_mixed value, as recorded in the GEMS Registry, equal to or greater than the
        Minimum Residential HSPF_mixed value for the same Product Type and Cooling Capacity in Table D16.4; or<br />
        b. If it does not have a Residential HSPF_mixed value recorded in the GEMS Registry, then it must have a Rated
        ACOP in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and
        Cooling Capacity in Table D16.5.<br />
        4. If the New End-User Equipment or replacement End-User Equipment has a Heating Capacity recorded in the GEMS Registry
        and is installed in the cold zone as defined in Table A27:<br />
        a. It must have a Residential HSPF_cold value, as recorded in the GEMS Registry, equal to or greater than the
        Minimum Residential HSPF_cold value for the same Product Type and Cooling Capacity in Table D16.4; or<br />
        b. If it does not have a Residential HSPF_cold value recorded in the GEMS Registry, then it must have a Rated ACOP
        in the GEMS Registry equal to or greater than the Minimum Rated ACOP for the same Product Type and Cooling
        Capacity in Table D16.5.
        """
    }


class HVAC1_HSPF_mixed_eligible(Variable):
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


class HVAC1_ACOP_eligible(Variable):
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


class HVAC1_HSPF_cold_eligible(Variable):
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