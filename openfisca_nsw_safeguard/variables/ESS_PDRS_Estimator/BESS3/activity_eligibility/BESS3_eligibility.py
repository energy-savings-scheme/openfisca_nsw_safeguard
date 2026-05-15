from openfisca_nsw_safeguard.base_variables import BaseVariable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_safeguard.entities import Building
import numpy as np


class BESS3_installation_final_activity_eligibility(BaseVariable):
    """
        Formula to calculate the BESS3 installation activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "BESS3 activity installation eligibility requirements",
        "variable-type": "output"
    }

    def formula(buildings, period, parameter):
       equipment_installation = buildings('BESS3_new_installation', period)
       apartment_dwellings = buildings('BESS3_apartment_dwellings', period)
       nmi = buildings('BESS3_nmi', period)
       engaged_acp = buildings('BESS3_engaged_ACP', period)
       minimum_payment = buildings('BESS3_minimum_payment', period)
       battery_capacity = buildings('BESS3_battery_capacity', period)
       length_battery_warranty = buildings('BESS3_length_battery_warranty', period)
       retainable_battery_capacity_warranty = buildings('BESS3_retainable_battery_capacity_warranty', period)
       approved_batteries_list = buildings('BESS3_approved_batteries_list', period)
       battery_inverter_output = buildings('BESS3_battery_inverter_output', period)
       installation_location = buildings('BESS3_installation_location', period)
       behind_meter = buildings('BESS3_behind_meter', period)
       approved_installer_list = buildings('BESS3_approved_installer_list', period)
       licensed_person = buildings('BESS3_licensed_person', period)
       internet_connectable = buildings('BESS3_internet_connectable', period)
       controlled_aggregator = buildings('BESS3_controlled_aggregator', period)


       end_formula = ( equipment_installation * apartment_dwellings * nmi * engaged_acp * minimum_payment * battery_capacity *
                       length_battery_warranty * retainable_battery_capacity_warranty * approved_batteries_list * battery_inverter_output *
                        installation_location * behind_meter * approved_installer_list * licensed_person * internet_connectable * controlled_aggregator)

       return end_formula