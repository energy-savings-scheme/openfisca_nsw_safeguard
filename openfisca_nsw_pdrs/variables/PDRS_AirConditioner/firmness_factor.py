from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


# Where to put global constants ? Do they need to be displayed?

RATIO_WEEKDAYS_TO_FULLWEEKS = float(5/7)
CONTRIBUTION_FACTOR = float(1)
NUMBER_OF_PEAK_WINDOW_HOURS = float(6*105)

class zone_type(Enum):
    hot="Hot"
    average="Average"
    cold="Cold"


class installation_purpose(Enum):
    residential='Residential/SME'
    commercial='Commercial'


class PDRS__Appliance__installation_purpose(Variable):
    # name="Appliance Installation Local Type" #alias
    entity=Building
    value_type=Enum
    possible_values=installation_purpose
    default_value=installation_purpose.residential
    definition_period=ETERNITY
    reference="Clause **"
    label="Is the air-conditioner(s) installed for Residential or Commercial purpose?" #wording as form input. check with Steve


# entity is not compulsory?

class PDRS__Air_Conditioner__load_factor(Variable):
    # name="Load Factor in computation of firmness factor" #specific to AC or general?
    reference=""
    entity=Building
    value_type=float
    definition_period=ETERNITY

    ##got the table: put it in
    # def formula(appliance, parameters):
    #     installation_purpose = appliance('PDRS__Appliance__installation_purpose')


