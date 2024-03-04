from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building



class RF1_get_network_loss_factor_by_postcode(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'input',
        'sorting' : 2,
        'label' : 'Network loss factor is calculated automatically from your postcode. If you have a 0 here, please check your postcode is correct. If the postcode has more than one distribution network service provider, we have chosen the network factor loss with the lowest value.'
    }
    def formula(building, period, parameters):
        postcode = building('RF1_PDRS__postcode', period)
        network_loss_factor = parameters(period).PDRS.table_network_loss_factor_by_postcode

        return network_loss_factor.calc(postcode)


class RF1_peak_demand_savings_capacity(Variable):
    reference = 'peak demand savings capacity'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
        baseline_peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['baseline_peak_adjustment']['RF1']
        baseline_input_power = 0.093
        peak_adjustment_factor = parameters(period).PDRS.table_A4_adjustment_factors['peak_adjustment']['RF1']
        input_power = 0
        firmness_factor = 1
        temp1 = (baseline_peak_adjustment_factor * baseline_input_power)
        temp2 = (input_power * peak_adjustment_factor )
        
        return ((temp1 - temp2) * firmness_factor)
    

class RF1_peak_demand_reduction_capacity(Variable):
    reference = 'peak demand reduction capacity'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    metadata = {
        'variable-type': 'inter-interesting'
    }

    def formula(buildings, period, parameters):
      peak_demand_savings_capacity = buildings('RF1_peak_demand_savings_capacity', period)
      summer_peak_demand_reduction_duration = 6
      lifetime = 7
      number_of_fridges = buildings('RF1_number_of_refrigerator_freezers_removal', period)

      return peak_demand_savings_capacity * summer_peak_demand_reduction_duration * lifetime * number_of_fridges