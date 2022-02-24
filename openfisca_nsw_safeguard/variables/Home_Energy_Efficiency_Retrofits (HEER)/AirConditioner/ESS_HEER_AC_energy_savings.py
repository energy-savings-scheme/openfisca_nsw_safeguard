from email.mime import base
import numpy as np
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_core.variables import Variable
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021



class ESS_HEER_AC_electricity_savings(Variable):
    value_type = float
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'What are the electricity savings created by installing a new AC or replacing an existing AC?'
    metadata = {
        'alias': "HEER AC Electricity Savings",
    }

    def formula(buildings, period, parameters):
        activity_type = buildings('Appliance__installation_type', period)
        ActivityType = activity_type.possible_values
        installation_electricity_savings = buildings(
            'ESS_HEER_AC_install_electricity_savings', period)
        replacement_electricity_savings = buildings(
            'ESS_HEER_AC_replace_electricity_savings', period)
        electricity_savings = np.select(
            [
                (activity_type == ActivityType.install),
                (activity_type == ActivityType.replacement)
            ],
            [
                installation_electricity_savings,
                replacement_electricity_savings
            ]
            )
        return electricity_savings