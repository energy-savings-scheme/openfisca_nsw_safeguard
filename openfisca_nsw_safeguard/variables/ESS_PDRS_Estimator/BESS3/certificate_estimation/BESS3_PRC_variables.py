from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_nsw_safeguard.entities import Building
from openfisca_core.periods import ETERNITY


class BESS3_postcode(BaseVariable):
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


class BESS3_battery_capacity_input(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'user-input',
        'label': 'Battery capacity (kWh)',
        'display_question' : 'What is the battery capacity (kWh)?',
        'sorting' : 2,
    }


class BESS3_number_of_dwellings_input(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'user-input',
        'label': 'Number of dwellings',
        'display_question' : 'What is the total number of dwellings?',
        'sorting' : 3,
    }


class BESS3_inverter_output_input(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'user-input',
        'label': 'Inverter output (kW)',
        'display_question' : 'What is the battery inverter output?',
        'sorting' : 4,
    }


class BESS3_solar_or_battery_only(BaseVariable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'user-input',
        'label': 'Solar or battery only',
        'display_question' : 'Is the battery installed within 90 days of new solar PV?',
        'sorting' : 5,
    }
