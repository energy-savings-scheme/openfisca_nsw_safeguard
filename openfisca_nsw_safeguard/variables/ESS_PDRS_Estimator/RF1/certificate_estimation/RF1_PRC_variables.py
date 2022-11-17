from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class RF1_DNSP_Options(Enum):
    Ausgrid = 'Ausgrid'
    Endeavour = 'Endeavour'
    Essential = 'Essential'


class RF1_DNSP(Variable):
    # this variable is used as the second input on all estimator certificate calculation pages
    value_type = Enum
    entity = Building
    possible_values = RF1_DNSP_Options
    default_value = RF1_DNSP_Options.Ausgrid
    definition_period = ETERNITY
    label = "Distribution Network Service Provider"
    metadata = {
        'variable-type': 'user-input',
        'label': 'Distribution Network Service Provider',
        'display_question': 'Who is your Distribution Network Service Provider?',
        'sorting' : 2
    }


class RF1_network_loss_factor(Variable):
    reference = 'table_A3_network_loss_factors'
    value_type = float
    entity = Building
    definition_period = ETERNITY
    
    def formula(buildings, period, parameters):
        distribution_district = buildings('RF1_DNSP', period)
        network_loss_factor = parameters(period).PDRS.table_A3_network_loss_factors['network_loss_factor'][distribution_district]
        return network_loss_factor


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

      return peak_demand_savings_capacity * summer_peak_demand_reduction_duration * lifetime

