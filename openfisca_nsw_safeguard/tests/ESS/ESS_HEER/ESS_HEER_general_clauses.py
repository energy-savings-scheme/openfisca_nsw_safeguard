from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS__HEER_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the Electricity Savings created from a HEER Implementation, in MWh?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "ESS HEER Electricity Savings",
    }

    def formula(buildings, period, parameters):

        method_type = buildings('ESS__method_type', period)
        MethodType = method_type.possible_values
        activity_definition = buildings('ESS_activity_definition', period)
        ActivityDefinition = activity_definition.possible_values

        is_HEER_activity_definition = (method_type == MethodType.clause_9_8_HEER)

        meets_HEER_general_requirements = buildings(
            'ESS__HEER_meets_all_general_requirements', period)

        is_HEER_activity_that_meets_general_requirements = (
            is_HEER_activity_definition *
            meets_HEER_general_requirements
        )

        electricity_savings = np.select([
            (activity_definition == ActivityDefinition.E1),
            (activity_definition == ActivityDefinition.E2),
        ],
        [
            buildings('ESS_HEER_lighting_replace_halogen_downlight_with_LED_electricity_savings', period),
            buildings('ESS_HEER_replace_halogen_floodlight_electricity_savings', period)
        ])
        return(
            is_HEER_activity_that_meets_general_requirements *
            electricity_savings
        )

class ESS__HEER_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the Electricity Savings created from a HEER Implementation, in MWh?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "ESS HEER Electricity Savings",
    }


class ESS_HEERActivityType(Enum):
    replace_glazed_window_or_door = 'Activity is replacing a glazed window or door.'
    modify_glazed_window_or_door = 'Activity is replacing a glazed window or door.'
    replace_pool_pump = 'Activity is replacing a pool pump.'
    install_ceiling_insulation_in_uninsulated_space = u'Activity is installing ceiling insulation' \
                                                       ' in an uninsulated space.'
    install_ceiling_insulation_in_unnder_insulated_space = u'Activity is installing ceiling insulation' \
                                                            ' in an under insulated space.'
    install_underfloor_insulation = u'Activity is installing under-floor insulation.'
    install_wall_insulation = u'Activity is installing wall insulation.'
    replace_gas_fired_heater_with_HE_water_heater = u'Activity is replacing a gas fired heater' \
                                                    ' with a high efficiency water heater.'
    install_or_replace_with_HE_gas_heater = u'Activity is installing a high efficiency gas heater' \
                                            ' or replacing an existing gas space heater with a high efficiency' \
                                            ' gas heater.'
    install_natural_roof_space_ventilator = 'Activity is installing a natural roof space ventilator.'
    install_fan_forced_pv_or_occupied_space_ventilator = u'Activity is installing a fan forced roof space ventilator,' \
                                                          ' installing a PV powered fan forced space ventilator, or' \
                                                          ' installing an occupied space ventilator.'
    replace_exhaust_fan = 'Activity is replacing an exhaust fan.'
    install_or_replace_with_HE_air_con = u'Activity is installing a high efficiency air conditioner' \
                                         ' or replacing an existing air conditioner with a high efficiency air conditioner.'
    replace_electric_water_heater_with_air_source_water_heater = u'Activity is replacing an existing electric water heater with' \
                                                          ' an air source heat pump water heater.'
    replace_electric_water_heater_with_solar_water_heater = u'Activity is replacing an existing electric water heater with' \
                                                          ' an solar heat pump water heater.'
    replace_gas_water_heater_with_air_source_water_heater = u'Activity is replacing an existing gas water heater with' \
                                                          ' an air source heat pump water heater.'
    replace_gas_water_heater_with_solar_electric_boosted_water_heater = u'Activity is replacing an existing gas water heater with' \
                                                                        ' an solar electric boosted heat pump water heater.'
    replace_gas_water_heater_with_solar_gas_boosted_water_heater = u'Activity is replacing an existing gas water heater with' \
                                                                        ' an solar gas boosted heat pump water heater.'
    replace_halogen_with_LED = 'Activity is replacing a halogen with an LED.'
    replace_linear_halogen_with_high_efficiency_lamp = 'Activity is replacing a linear halogen with a high efficiency lamp.'
    replace_PAR_with_efficiency_lamp = 'Activity is replacing a PAR with an efficient lamp.'
    replace_T8_or_T12_with_LED = 'Activity is replacing a T8 or T12 luminaire with an LED.'
    replace_showerhead_with_low_flow_showerhead = 'Activity is replacing a showerhead with a low flow showerhead.'
    modify_external_door_with_draught_proofing = 'Activity is modifying an external door with draught proofing.'
    modify_external_window_with_draught_proofing = 'Activity is modifying an external window with draught proofing.'
    modify_fireplace_chimney_with_damper = 'Activity is modifying a fireplace chimney by sealing with a damper.'
    install_external_blind = 'Activity is installing an external blind to a window or door.'
    modify_exhaust_fan = 'Activity is modifying an exhaust fan with a sealing product.'


class ESS__HEER_activity_type(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the Electricity Savings created from a HEER Implementation, in MWh?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "ESS HEER Electricity Savings",
    }
