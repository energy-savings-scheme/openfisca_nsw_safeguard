from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

# This file defines Appliance specific variables consistent through PDRS


class zone_type(Enum):
    hot = "Hot"
    average = "Average"
    cold = "Cold"


class Appliance__zone_type(Variable):
    entity = Building
    value_type = Enum
    possible_values = zone_type
    default_value = zone_type.average
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the Zone type of the area?"
    metadata = {
        'alias': "Zone Type",
        'activity-group': "Air Conditioners?",
        'activity-name': "Replace or Install an Air Conditioner",
        'variable-type': "input"
    }


class installation_purpose(Enum):
    residential = 'Residential/SME'
    commercial = 'Commercial'


class Appliance__installation_purpose(Variable):
    entity = Building
    value_type = Enum
    possible_values = installation_purpose
    default_value = installation_purpose.residential
    definition_period = ETERNITY
    reference = "Clause **"
    # wording as form input.
    label = "Is the air-conditioner(s) installed for Residential or Commercial purpose?"
    metadata = {
        'alias': "Residential or Commercial?",
        'activity-group': "Air Conditioners?",
        'activity-name': "Replace or Install an Air Conditioner",
        'variable-type': "input"
    }


class installation_type(Enum):
    install = "Installation of a new product"
    replacement = "Replacement of an old product"


class Appliance__installation_type(Variable):
    # name="New or Replacement?"
    reference = ""
    value_type = Enum
    possible_values = installation_type
    default_value = installation_type.install
    entity = Building
    definition_period = ETERNITY
    label = "Is it a new installation or a replacement?"
    metadata = {
        "variable-type": "input",
        "alias": "New or Replacement?",
    }
