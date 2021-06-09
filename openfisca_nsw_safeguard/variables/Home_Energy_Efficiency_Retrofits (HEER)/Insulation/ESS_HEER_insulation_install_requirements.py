from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Building
from openfisca_nsw_safeguard.regulation_reference import ESS_2021
import numpy as np


class ESS__HEER_insulation_install_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the insulation implementation meet all of the Eligibility' \
            ' Requirements?'
    metadata = {
        'alias': "Install insulation meets eligibility requirements",
        "regulation_reference": ESS_2021["8", "8.8"]
    }

    def formula(buildings, period, parameters):
        no_existing_insulation = np.logical_not(buildings, 'ESS__HEER_insulation_existing_insulation', period)
        return no_existing_insulation


class ESS__HEER_insulation_install_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the insulation implementation meet all of the Equipment' \
            ' Requirements?'
    metadata = {
        'alias': "Install insulation meets equipment requirements",
        "regulation_reference": ESS_2021["8", "8.8"]
    }

    def formula(buildings, period, parameters):
        meets_performance_requirements = np.logical_not(buildings('ESS__HEER_insulation_meets_AS4859_performance_requirements', period))
        achieves_minimum_R_value = buildings('ESS__HEER_insulation_meets_minimum_R_value', period)
        has_25_year_warranty_length = buildings('ESS__HEER_has_25_year_warranty', period)
        is_not_foil_insulation = np.logical_not(buildings('ESS__HEER_insulation_is_foil', period))