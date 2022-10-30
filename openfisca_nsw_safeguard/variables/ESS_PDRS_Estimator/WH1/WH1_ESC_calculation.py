from xml.etree import ElementInclude
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class WH1_capacity_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Capacity Factor'
    metadata = {
        "variable-type": "inter-interesting"
    }

    def formula(buildings, period, parameters):
      HP_Cap = buildings('WH1_HP_capacity_factor', period)
      WH_Cap = buildings('WH1_WH_capacity_factor', period)

      capacity_factor = np.select(
                                 [
                                    (HP_Cap <= WH_Cap),
                                    (HP_Cap > WH_Cap)
                                 ],
                                 [
                                    1,
                                    WH_Cap / HP_Cap
                                 ]
                                 )

      return capacity_factor


class WH1_deemed_activity_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity gas savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      HP_gas = buildings('WH1_HP_gas', period)
      capacity_factor = buildings('WH1_capacity_factor', period)
      lifetime = parameters(period).ESS.HEAB.table_F16_1.lifetime

      gas_savings = -(HP_gas) * capacity_factor * (lifetime / 3.6)

      return gas_savings


class WH1_Ref_Elec(Variable):
    """ Annual Electrical Energy used by a reference electric resistance water heater in a year
    """
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Reference electricity'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        com_peak_load = buildings('WH1_com_peak_load', period)

        # we divide this by 1000 to convert MJ to GJ
        ref_elec = 365 * 0.905 * 1.05 * (com_peak_load / 1000)
        return ref_elec


class WH1_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        ref_elec = buildings('WH1_Ref_Elec', period)
        hp_elec = buildings('WH1_HP_elec', period)
        capacity_factor = buildings('WH1_capacity_factor', period)
        lifetime = parameters(period).ESS.HEAB.table_F16_1['lifetime']

        electricity_savings = (ref_elec - hp_elec) * capacity_factor * (lifetime / 3.6)
        return electricity_savings


class WH1_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Electricity savings'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        deemed_activity_electricity_savings = buildings('WH1_deemed_activity_electricity_savings', period)
        regional_network_factor = buildings('WH1_regional_network_factor', period)

        electricity_savings = deemed_activity_electricity_savings * regional_network_factor
        return electricity_savings


class WH1_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for WH1'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('WH1_electricity_savings', period)
        electricity_certificate_conversion_factor = 1.06
        gas_savings = buildings('WH1_deemed_activity_gas_savings', period) #gas savings and deemed activity gas savings are the same value
        gas_certificate_conversion_factor = 0.39

        result = np.rint((electricity_savings * electricity_certificate_conversion_factor) + (gas_savings * gas_certificate_conversion_factor))
        result_to_return = np.select([
                result < 0, result > 0
            ], [
                0, result
            ])
        return result_to_return
