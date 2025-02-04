from distutils.command.build import build
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class BESS1_PDRSDec24_installation_final_activity_eligibility(Variable):
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
       equipment_installation = buildings('BESS1_PDRSDec24_new_installation', period)
       new_solar_battery = buildings('BESS1_PDRSDec24_new_solar_battery', period)
       solar_panels = buildings('BESS1_PDRSDec24_solar_panels', period)
       ACP_engaged = buildings('BESS1_PDRSDec24_engaged_ACP', period)
       minimum_payment = buildings('BESS1_PDRSDec24_minimum_payment', period)
       battery_capacity = buildings('BESS1_PDRSDec24_battery_capacity', period)
       battery_warranty_length = buildings('BESS1_PDRSDec24_length_battery_warranty', period)
       battery_warranty_retainable_capacity = buildings('BESS1_PDRSDec24_retainable_battery_capacity_warranty', period)
       has_inverter_and_warranty_length_eligible = buildings('BESS1_has_inverter_and_warranty_length_eligible', period) 
       battery_warranty_temperature_range = buildings('BESS1_PDRSDec24_temperature_range_warranty', period)
       battery_warranty_throughput_before_April_2026 = buildings ('BESS1_PDRSDec24_minimum_throughput_warranty_before_April_2026', period)
       installation_location_eligible = buildings('BESS1_PDRSDec24_installation_location_eligible', period)
       installed_indoors_has_smoke_alarm = buildings('BESS1_PDRSDec24_installed_indoors_has_smoke_alarm', period)
       battery_internet_connectable = buildings('BESS1_PDRSDec24_battery_internet_connectable', period)
       battery_controllable_third_party = buildings('BESS1_PDRSDec24_battery_controllable_third_party', period)
       approved_product_list = buildings('BESS1_PDRSDec24_approved_product_list', period)
       approved_installer = buildings('BESS1_PDRSDec24_approved_installer', period)
       DER_Register = buildings('BESS1_PDRSDec24_DER_register', period)

       end_formula = ( equipment_installation * new_solar_battery * solar_panels * ACP_engaged * minimum_payment * battery_capacity * 
                       battery_warranty_length * battery_warranty_retainable_capacity * has_inverter_and_warranty_length_eligible * battery_warranty_temperature_range * battery_warranty_throughput_before_April_2026 *
                       installation_location_eligible * installed_indoors_has_smoke_alarm * battery_internet_connectable * battery_controllable_third_party * 
                       approved_product_list * approved_installer * DER_Register)

       return end_formula