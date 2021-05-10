from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021


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
        "regulation_reference": ESS_2021["XX", "GA"]
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
    label = "Is the air-conditioner(s) installed for Residential or Commercial purpose?"
    metadata = {
        'alias': "Residential or Commercial?",
        "regulation_reference": ESS_2021["XX", "GA"]
    }


class installation_type(Enum):
    install = "Installation of a new product"
    replacement = "Replacement of an old product"


class Appliance__installation_type(Variable):
    reference = ""
    value_type = Enum
    possible_values = installation_type
    default_value = installation_type.install
    entity = Building
    definition_period = ETERNITY
    label = "Is it a new installation or a replacement?"
    metadata = {
        "alias": "New or Replacement?",
        "regulation_reference": ESS_2021["XX", "GA"]
    }
