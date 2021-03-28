from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class PDRS__ROOA__firmness_factor(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    metadata ={
        'alias' : "Firmness Factor",
        'activity-group' : "Removal Of Old Appliances", 
        'activity-name' : "Removal of a Spare Refrigerator or Freezer",    
        'variable-type' : "intermediary"    
    }

    def formula(building, period, parameters):
        load_factor = parameters(period).ROOA_load_factors_table
        contribution_factor = parameters(period).ROOA_related_constants.CONTRIBUTION_FACTOR
        duration_factor = parameters(period).ROOA_related_constants.DURATION_FACTOR
        # note that this isn't the same duration factor as in AC. I wonder if we should give it a different name somehow? any confusion?
        return contribution_factor*load_factor*duration_factor
