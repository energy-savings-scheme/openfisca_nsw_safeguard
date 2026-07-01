from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building
import numpy as np


class BESS2_V5Nov24_installation_final_activity_eligibility(BaseVariable):
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
        demand_response_contract = buildings('BESS2_V5Nov24_demand_response_contract', period)
        existing_solar_battery = buildings('BESS2_V5Nov24_existing_solar_battery', period)
        BCA_class_1 = buildings('BESS2_V5Nov24_BCA_class_1', period)
        life_support_equipment = buildings('BESS2_V5Nov24_life_support_equipment', period)
        approved_battery_list = buildings('BESS2_V5Nov24_approved_battery_list', period)
        battery_capacity = buildings('BESS2_V5Nov24_battery_capacity', period)
        battery_warranty_length = buildings('BESS2_V5Nov24_length_battery_warranty', period)
        equipment_warranty = buildings('BESS2_V5Nov24_equipment_warranty', period)
        battery_internet_connectable = buildings('BESS2_V5Nov24_internet_connectable', period)
        ACP_engaged = buildings('BESS2_V5Nov24_engaged_ACP', period)

        end_formula = (demand_response_contract * existing_solar_battery * BCA_class_1 * life_support_equipment * 
                       approved_battery_list * battery_capacity * battery_warranty_length * equipment_warranty * 
                       battery_internet_connectable * ACP_engaged)

        return end_formula