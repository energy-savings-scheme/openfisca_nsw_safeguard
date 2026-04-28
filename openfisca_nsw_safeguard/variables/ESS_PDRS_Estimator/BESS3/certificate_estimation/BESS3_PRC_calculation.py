import numpy as np

from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_nsw_safeguard.entities import Building
from openfisca_core.periods import ETERNITY


class BESS3_PDRS__nominal_battery_capacity(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'output',
    }

    def formula(building, period, parameters):
        nominal_battery_capacity_input = building('BESS3_PDRS__nominal_battery_capacity_input', period)
        
        return nominal_battery_capacity_input * 90 / 100


class BESS3_PDRS__number_of_dwellings(BaseVariable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'output',
    }

    def formula(building, period, parameters):
        number_of_dwellings_input = building('BESS3_PDRS__number_of_dwellings_input', period)
        
        return number_of_dwellings_input * 5 # kWh
    

class BESS3_PDRS__inverter_rated_discharge_power(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'output',
    }

    def formula(building, period, parameters):
        inverter_rated_discharge_power_input = building('BESS3_PDRS__inverter_rated_discharge_power_input', period)
        
        return inverter_rated_discharge_power_input * 4


class BESS3_PDRS__usable_battery_capacity(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'output',
    }

    def formula(building, period, parameters):
        nominal_battery_capacity = building('BESS3_PDRS__nominal_battery_capacity', period)
        number_of_dwellings = building('BESS3_PDRS__number_of_dwellings', period)
        inverter_rated_discharge_power = building('BESS3_PDRS__inverter_rated_discharge_power', period)

        return min(nominal_battery_capacity, number_of_dwellings, inverter_rated_discharge_power)


class BESS3_PDRS__demand_shifting_component(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'output',
    }

    def formula(building, period, parameters):
        usable_battery_capacity = building('BESS3_PDRS__usable_battery_capacity', period)
        is_solar_or_battery_only = building('BESS3_PDRS__solar_or_battery_only', period)

        result = np.select(
            [is_solar_or_battery_only],
            [usable_battery_capacity * 0.12],
            default=usable_battery_capacity * 0.0853
        )

        return result


class BESS3_PDRS__peak_demand_shifting_capacity(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'output',
    }

    def formula(building, period, parameters):
        demand_shifting_component = building('BESS3_PDRS__demand_shifting_component', period)
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor['firmness_factor']['BESS3']
        return demand_shifting_component * firmness_factor


class BESS3_PDRS__peak_demand_reduction_capacity(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'output',
    }

    def formula(building, period, parameters):
        peak_demand_shifting_capacity = building('BESS3_PDRS__peak_demand_shifting_capacity', period)
        summer_peak_demand_reduction_duration = 6
        lifetime = 15
        return peak_demand_shifting_capacity * summer_peak_demand_reduction_duration * lifetime


class BESS3_PDRS__peak_demand_savings(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'output',
    }

    def formula(building, period, parameters):
        peak_demand_reduction_capacity = building('BESS3_PDRS__peak_demand_reduction_capacity', period)
        return peak_demand_reduction_capacity


class BESS3_PDRS__PRC_calculation(BaseVariable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata= {
        'variable-type' : 'output',
        'label': 'Peak Reduction Capacity (PRC) kW',
    }

    def formula(building, period, parameters):
        postcode = building('BESS3_PDRS__postcode', period)
        peak_demand_reduction_capacity = building('BESS3_PDRS__peak_demand_reduction_capacity', period)
        network_loss_factor = parameters(period).PDRS.table_network_loss_factor_by_postcode.calc(postcode)

        return peak_demand_reduction_capacity * network_loss_factor * 10
