from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022


class PDRS_HEAB_motors_install_peak_demand_savings(BaseVariable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "HEAB Motors Install The Peak demand savings "
    metadata = {
        "alias": "HEAB Motors Install Peak demand savings",
        "regulation_reference": PDRS_2022["HEAB", "motors_install", "energy_savings"]
    }

    def formula(building, period, parameters):

        meets_all_requirements = building(
            'PDRS_motor_install_meets_all_requirements', period)
        savings = building("PDRS_motors_peak_demand_savings", period)

        return meets_all_requirements * savings
