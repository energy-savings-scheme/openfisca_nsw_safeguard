from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class BESS1_installation_final_activity_eligibility(Variable):
    """
        Formula to calculate the BESS1 installation activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "alias": "BESS1 activity installation eligibility requirements",
        "variable-type": "output"
    }

    def formula(buildings, period, parameter):
       equipment_installation = buildings('BESS1_new_installation', period)
       new_solar_battery = buildings('BESS1_new_solar_battery', period)
       solar_panels = buildings('BESS1_solar_panels', period)
       ACP_engaged = buildings('BESS1_engaged_ACP', period)
       minimum_payment = buildings('BESS1_minimum_payment', period)
       battery_capacity = buildings('BESS1_battery_capacity', period)
       battery_warranty = buildings('BESS1_battery_warranty', period)
       battery_internet_connectable = buildings('BESS1_battery_internet_connectable', period)
       battery_controllable_third_party = buildings('BESS1_battery_controllable_third_party', period)
       approved_list = buildings('BESS1_approved_list', period)
       qualified_install = buildings('BESS1_equipment_installation', period)
       DER_Register = buildings('BESS1_DER_register', period)



       end_formula = ( equipment_installation * new_solar_battery * solar_panels * ACP_engaged * 
                       minimum_payment * battery_capacity * battery_warranty * battery_internet_connectable *
                       battery_controllable_third_party * approved_list * qualified_install * DER_Register)

       return end_formula