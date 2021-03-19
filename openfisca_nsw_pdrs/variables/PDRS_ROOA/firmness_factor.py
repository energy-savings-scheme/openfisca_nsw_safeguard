from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


# Where to put global constants ? Do they need to be displayed?


class PDRS__ROOA__firmness_factor(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY

    def formula(building, period, parameters):
        load_factor = parameters(period).ROOA_load_factors_table
        contribution_factor = parameters(period).ROOA_related_constants.CONTRIBUTION_FACTOR
        ## call the duration factor computed from above? How to call the formula under PDRS__Air_Conditioner__duration_factor ?
        duration_factor = parameters(period).ROOA_related_constants.DURATION_FACTOR
        # note that this isn't the same duration factor as in AC.
        return contribution_factor*load_factor*duration_factor
