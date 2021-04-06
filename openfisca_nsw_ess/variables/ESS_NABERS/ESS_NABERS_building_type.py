from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class NABERS_BuildingType(Enum):
    aged_care = 'Building is an residential aged care building.'
    apartment_building = 'Building is an apartment building.'
    data_centre = 'Building is a data centre.'
    hospital = 'Building is a hospital.'
    hotel = 'Building is a hotel.'
    office = 'Building is an office.'
    retirement_living = 'Building is a retirement living building.'
    shopping_centre = 'Building is a shopping centre.'


class ESS__NABERS_building_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = NABERS_BuildingType
    default_value = NABERS_BuildingType.office
    definition_period = ETERNITY
    label = 'What is the building type for the NABERS rated building?'


class postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = "What is the postcode for the building you are calculating ESCs for?"
