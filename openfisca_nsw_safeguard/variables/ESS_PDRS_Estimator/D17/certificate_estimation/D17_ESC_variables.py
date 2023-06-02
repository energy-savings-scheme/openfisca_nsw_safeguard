from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


""" Parameters for D17 ESC Calculation
    These variables use Rule tables and IPART Registry data
"""


#get the postcode and calculate the heat pump zone

class D17_get_zone_by_postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "Zone"
    }
    def formula(building, period, parameters):
        postcode = building('D17_PDRS__postcode', period)
        zones = parameters(period).ESS.ESS_general.Postcode_zones_air_source_heat_pumps
        return zones.calc(postcode)
    

class D17_PDRS__postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata={
        'variable-type' : 'user-input',
        'alias' : 'PDRS Postcode',
        'display_question' : 'Postcode where the installation has taken place',
        'sorting' : 1,
        'label': 'Postcode'
    }


#get the heat pump zone, brand and model and calculate the Bs and Be
#get the brand and model, find the system size value and calculate the Baseline A


class D17_Baseline_A(Variable):
    #pulls from table D17.1
    value_type = int
    entity = Building
    definition_period = ETERNITY
    
    system_size = by brand and model

    baseline_A = parameters(period).ESS.HEER.table_D17.1[system_size]


class D17_Bs(Variable):
    #baseline energy consumption
    value_type = int
    entity = Building
    definition_period = ETERNITY
   
    def formula(buildings, period, parameters):
        
        heat_pump_zone = buildings('D17_get_zone_by_postcode', period)

        
        baseline_energy_consumption = parameters(period).

        return baseline_energy_consumption




class D17_Be(Variable):
    #annual electricity usage
    value_type = int
    entity = Building
    definition_period = ETERNITY
    metadata={
        

    }