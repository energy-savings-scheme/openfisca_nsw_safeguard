from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

# This file defines Appliance specific variables consistent through PDRS

class zone_type(Enum):
    hot="Hot"
    average="Average"
    cold="Cold"

class PDRS__Appliance__zone_type(Variable):
    entity=Building
    value_type=Enum
    possible_values=zone_type
    default_value=zone_type.average
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the Zone type of the area?"
    metadata ={
        'alias' : "Zone Type",
        'activity-group' : "Air Conditioners?",
        'activity-name' : "Replace or Install an Air Conditioner",
        'variable-type' : "input"
    }

class installation_purpose(Enum):
    residential='Residential/SME'
    commercial='Commercial'


class PDRS__Appliance__installation_purpose(Variable):
    entity=Building
    value_type=Enum
    possible_values=installation_purpose
    default_value=installation_purpose.residential
    definition_period=ETERNITY
    reference="Clause **"
    label="Is the air-conditioner(s) installed for Residential or Commercial purpose?" #wording as form input.
    metadata ={
        'alias' : "Residential or Commercial?",
        'activity-group' : "Air Conditioners?",
        'activity-name' : "Replace or Install an Air Conditioner",
        'variable-type' : "input"
    }

