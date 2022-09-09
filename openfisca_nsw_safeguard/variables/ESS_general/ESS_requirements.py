from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS_meets_overall_method_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the implementation meet the relevant Method-specific ' \
            ' requirements detailed in Clauses 7, 8 or 9?'

    def formula(buildings, period, parameters):


        meets_HEER_overall_requirements = buildings(
            'ESS__HEER_meets_all_general_requirements', period)
        meets_HEAB_overall_requirements = buildings(
            'ESS_HEAB_meets_all_general_requirements', period)
        

        ESS_method_type = buildings('ESS__method_type', period)
        ESS_MethodType = ESS_method_type.possible_values

        is_HEER_activity = (ESS_method_type == ESS_MethodType.clause_9_8_HEER)
        is_HEAB_activity = (ESS_method_type == ESS_MethodType.clause_9_9_HEAB)

#  note the above section a. pulls from the ESS_activity_definition variable, and b.
#  automatically sets the method type as 

        relevant_requirements = np.select(
                                            [
                                            is_HEER_activity,
                                            is_HEAB_activity
                                            ],
                                            [
                                                meets_HEER_overall_requirements,
                                                meets_HEAB_overall_requirements
                                            ]
                                            )

        return relevant_requirements