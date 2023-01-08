from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class SYS2_replacement_final_activity_eligibility(Variable):
    """
        Formula to calculate the SYS2 replacement activity eligibility
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        replacement = buildings('SYS2_equipment_replaced', period)
        old_equipment_installed_on_site = buildings('SYS2_old_equipment_installed_on_site', period)
        qualified_install = buildings('SYS2_qualified_install_removal', period)
        legal_disposal = buildings('SYS2_legal_disposal', period)
        registered_GEMS = buildings('SYS2_equipment_registered_in_GEMS', period)
        voluntary_labelling_scheme = buildings('SYS2_voluntary_labelling_scheme', period)
        star_rating_minimum_four_and_a_half = buildings('SYS2_star_rating_minimum_four_and_a_half', period)
        warranty = buildings('SYS2_warranty', period)
        single_phase = buildings('SYS2_single_phase', period)
        pump_not_single_speed = buildings('SYS2_not_single_speed', period)
        single_speed_input_power = buildings('SYS2_single_speed_input_power', period)
        multiple_speeds_input_power = buildings('SYS2_multiple_speeds_input_power', period)

        # check if it's registered in GEMS or the voluntary labelling scheme                                 
        GEMS_or_voluntary_labelling_scheme = (registered_GEMS * np.logical_not(voluntary_labelling_scheme)) + (np.logical_not(registered_GEMS) * voluntary_labelling_scheme)

        #single speed is YES and single speed input power is YES or multiple speed is YES and multiple speed input power is YES
        speed_and_input_power_eligible = (np.logical_not(pump_not_single_speed) * single_speed_input_power) + (pump_not_single_speed * multiple_speeds_input_power)

        end_formula = ( replacement * old_equipment_installed_on_site * qualified_install * 
                        legal_disposal * GEMS_or_voluntary_labelling_scheme * star_rating_minimum_four_and_a_half *
                        warranty * single_phase * speed_and_input_power_eligible )

        return end_formula