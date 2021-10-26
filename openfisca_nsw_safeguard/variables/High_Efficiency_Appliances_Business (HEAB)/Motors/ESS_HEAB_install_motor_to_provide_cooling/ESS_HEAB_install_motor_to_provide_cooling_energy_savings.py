from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np



class ESS_HEAB_install_motor_to_provide_cooling_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F5?'

    def formula(buildings, period, parameters):
        input_power = buildings('new_motor_nominal_input_power', period)
        nominal_input_power = select([input_power <= 34.00,
                                    input_power > 34.00],
                                    ["less_than_or_equal_to_34_kW",
                                    "more_than_34_kW"])
        coefficient_a = parameters(period).ESS.HEAB.table_F5_1.nominal_input_power.coefficient_a[nominal_input_power]
        coefficient_b = parameters(period).ESS.HEAB.table_F5_1.nominal_input_power.coefficient_b[nominal_input_power]
        control_system = buildings('F5_control_system', period)
        average_power = parameters(period).ESS.HEAB.table_F5_2.average_power[control_system]
        refrigerator_type = buildings('F5_refrigerator_type', period)
        coefficient_of_performance = parameters(period).ESS.HEAB.table_F5_3.system_type_COP[refrigerator_type]
        hours = parameters(period).ESS.HEAB.table_F5_3.hours[refrigerator_type]
        lifetime = parameters(period).ESS.HEAB.table_F5_4.lifetime
        MWh_conversion = parameters(period).general_ESS.unit_conversion_factors['kWh_to_MWh']
        return ((input_power * (coefficient_a - average_power) + coefficient_b)
               * (1 + (1 / coefficient_of_performance))
               * hours * lifetime / MWh_conversion)


class F5ControlSystem(Enum):
    no_control_system = 'The motor has no control system in place.'
    temperature_dependent_speed_control = 'The motor has a temperature dependent' \
                                          ' speed control in place.'
    pressure_dependent_speed_control = 'The motor has a pressure dependent' \
                                       ' speed control in place.'
    timer_speed_control = 'The control system has a timer speed control, which' \
                          ' is set on the low speed setting for at least 8 hours' \
                          ' per day.'
    # note we need to determine what happens in the case where the timer is not \
    # set to a minimum of 8 hours on low speed per day.


class F5_control_system(Variable):
    value_type = Enum
    entity = Building
    possible_values = F5ControlSystem
    default_value = F5ControlSystem.no_control_system
    definition_period = ETERNITY
    label = 'What is the control system for the new end user equipment to be' \
            ' installed within Activity Definition F5?'


class F5RefrigeratorSystemType(Enum):
    refrigerated_cabinet = 'Motor is installed in a refrigerated cabinet.'
    reach_in_freezer = 'Motor is installed in a reach_in_freezer.'
    cool_room = 'Motor is installed in a cool room.'


class F5_refrigerator_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = F5RefrigeratorSystemType
    default_value = F5RefrigeratorSystemType.refrigerated_cabinet
    definition_period = ETERNITY
    label = 'What is the refrigerator type that the new End User Equipment is' \
            ' being installed in, in Activity Definition F5?'


class F5_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the nominal input power of new End User Equipment at full' \
            ' throttle, with the impeller fitted?'
