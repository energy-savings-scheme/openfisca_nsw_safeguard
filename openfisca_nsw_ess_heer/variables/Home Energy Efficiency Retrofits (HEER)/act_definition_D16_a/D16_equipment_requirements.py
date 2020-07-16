# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

class D16a_is_listed_on_product_register(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment listed on a product register?'


class D16a_is_certified_to_AS_NZS_2712(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment certified to the standard of AS/NZS' \
            ' 2712?'
