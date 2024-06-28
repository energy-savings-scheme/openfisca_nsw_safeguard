import enum
from multiprocessing import pool
import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class SYS2_PDRSAug24_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
        PAEC = buildings('SYS2_PDRSAug24_projected_annual_energy_consumption', period)
        DRT = buildings('SYS2_PDRSAug24_daily_run_time', period)

        input_power = PAEC / (365 * DRT)
        return input_power



class SYS2_PDRSAug24_baseline_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY

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

        baseline_input_power = parameters(period).PDRS.pool_pumps.table_sys2_1_PDRSAug24.baseline_input_power[nameplate_input_power_to_check]
        return baseline_input_power


class SYS2_PDRSAug24_get_network_loss_factor_by_postcode(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'input',
        'sorting' : 2,
        'label' : 'Network loss factor is calculated automatically from your postcode. If you have a 0 here, please check your postcode is correct. If the postcode has more than one distribution network service provider, we have chosen the network factor loss with the lowest value.'
    }
    def formula(building, period, parameters):
        postcode = building('SYS2_PDRSAug24_PDRS__postcode', period)
        network_loss_factor = parameters(period).PDRS.table_network_loss_factor_by_postcode

        return network_loss_factor.calc(postcode)