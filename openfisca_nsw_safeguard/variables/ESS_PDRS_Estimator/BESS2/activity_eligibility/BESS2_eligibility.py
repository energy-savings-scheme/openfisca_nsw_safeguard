from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class BESS2_installation_final_activity_eligibility(Variable):
    """
        Formula to calculate the BESS1 installation activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "BESS2 activity installation eligibility requirements",
        "variable-type": "output"
    }

    def formula(buildings, period, parameter):
        demand_response_contract = buildings('BESS2_demand_response_contract', period)
        existing_solar_battery = buildings('BESS2_existing_solar_battery', period)
        solar_panels_existing_address = buildings('BESS2_solar_panels_existing_address', period)
        life_support_equipment = buildings('BESS2_life_support_equipment', period)
        battery_capacity = buildings('BESS2_battery_capacity', period)
        implementation_date = buildings('BESS2_implementation_date', period)
        battery_internet_connectable = buildings('BESS2_internet_connectable', period)
        approved_battery_list = buildings('BESS2_approved_battery_list', period)



        end_formula = (demand_response_contract * existing_solar_battery * solar_panels_existing_address * life_support_equipment *
                       battery_capacity * implementation_date * battery_internet_connectable * approved_battery_list)

        return end_formula