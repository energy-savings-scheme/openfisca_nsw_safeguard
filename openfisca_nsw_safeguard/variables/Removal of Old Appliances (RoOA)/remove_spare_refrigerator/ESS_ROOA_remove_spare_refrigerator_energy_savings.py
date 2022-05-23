from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021


class ESS_ROOA_remove_spare_refrigerator_energy_savings(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Eligibility' \
            ' Requirements defined in Removal of Old Appliance (fridge)?'
    metadata = {
        'alias': "ROOA meets eligibility requirements",
    }

    def formula(buildings, period, parameters):
        electricity_savings = 5.7
        meets_all_requirements = buildings('ESS_ROOA_remove_spare_refrigerator_meets_all_requirements', period)
        return (
            electricity_savings * 
            meets_all_requirements
        )