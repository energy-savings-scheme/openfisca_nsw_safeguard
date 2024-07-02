import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for SYS2 ESC Calculation
    These variables use Rule tables
"""
class SYS2_PDRSAug24_PDRS__postcode(Variable):
    # using to get the regional network factor and network loss factor
    # this variable is used as the first input on all estimator certificate calculation pages
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'user-input',
        'alias' : 'PDRS Postcode',
        'label': 'Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1
    }


class SYS2_PDRSAug24_nameplate_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'input',
        'label': 'Nameplate Input Power (w)',
        'display_question' : 'The input power of the new or replacement pool pump as recorded in the GEMS Registry',
        'sorting' : 2
    }


class SYS2_PDRSAug24_projected_annual_energy_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'input',
        'label': 'PAEC (kWh/year)',
        'display_question' : 'The projected annual energy consumption of the new or replacement pool pump as recorded in the GEMS Registry',
        'sorting' : 3
    }


class SYS2_PDRSAug24_daily_run_time(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type' : 'input',
        'label': 'DRT (hours/day)',
        'display_question' : 'The daily run time of the new or replacement pool pump as recorded in the GEMS Registry',
        'sorting' : 4
    }


class SYS2_PDRSAug24_PAEC_baseline(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": 'output'
    }

    def formula(buildings, period, parameters):
        nameplate_input_power = buildings('SYS2_PDRSAug24_nameplate_input_power', period)

        nameplate_input_power_to_check = np.select(
            [
                (nameplate_input_power <= 1000),
                (nameplate_input_power > 1000) * (nameplate_input_power <= 1500),
                (nameplate_input_power > 1500) * (nameplate_input_power <= 2000),
                (nameplate_input_power > 2000),
            ],
            [
                'less_than_or_equal_to_1000w',
                '1001_to_1500w',
                '1501_to_2000w',
                'greater_than_2000w'
            ])

        PAEC_baseline = parameters(period).ESS.HEER.table_D5_1_PDRSAug24.baseline_PAEC[nameplate_input_power_to_check]
        return PAEC_baseline