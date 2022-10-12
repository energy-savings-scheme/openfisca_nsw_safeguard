import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


""" Parameters for WH1 ESC Calculation
    These variables use VEU Registry data
"""
class WH1_HP_capacity_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY


class WH1_WH_capacity_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY


class WH1_HP_gas(Variable):
    #Annual Gas Energy used by the End-User equipment
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY


class WH1_com_peak_load(Variable):
    #Peak daily winter load
    reference = 'Mj per day'
    value_type = float
    entity = Building
    definition_period = ETERNITY


class WH1_HP_elec(Variable):
    #Annual Electrical Energy used by the End-User equipment
    reference = 'Gj per year'
    value_type = float
    entity = Building
    definition_period = ETERNITY


""" These variables use Rule tables
"""
class WH1_postcode(Variable):
    #Postcode
    value_type = int
    entity = Building
    definition_period = ETERNITY


class WH1_regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor from ESS Table A24'
    
    def formula(buildings, period, parameters):
        postcode = buildings('WH1_postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided


