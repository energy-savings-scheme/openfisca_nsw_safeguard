from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_nsw_safeguard.entities import Building
from openfisca_core.periods import ETERNITY


class BESS3_PDRS__postcode(BaseVariable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'user-input',
        'label': 'Postcode',
        'alias' : 'PDRS Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1,
    }


class BESS3_PDRS__nominal_battery_capacity_input(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'user-input',
        'label': 'Nominal battery capacity (kWh)',
        'display_question' : 'What is the Nominal Battery Capacity (kWh) as recorded?',
        'sorting' : 2,
    }


class BESS3_PDRS__number_of_dwellings_input(BaseVariable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'user-input',
        'label': 'Number of dwellings',
        'display_question' : 'What is the total number of lot dwellings?',
        'sorting' : 3,
    }


class BESS3_PDRS__inverter_rated_discharge_power_input(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'user-input',
        'label': 'Inverter rated discharge power (kW)',
        'display_question' : 'What is the Inverter Rated Discharge Power (kW)?',
        'sorting' : 4,
    }


class BESS3_PDRS__solar_or_battery_only(BaseVariable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'user-input',
        'label': 'Solar or battery only',
        'display_question' : 'Is the battery installed within 90 days of new Solar PV?',
        'sorting' : 5,
    }
