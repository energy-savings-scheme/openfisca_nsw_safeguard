# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F7_motor_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the motor been installed?'


class F7_output_between_0_73_and_185_kW(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the motor\'s rated output between 0.73 kW and 185kW?'

    def formula(buildings, period, parameters):
        rated_output = buildings('F7_rated_output', period)
        between_0_73_and_185_kW = (rated_output >= 0.73 and rated_output <= 185)
        return between_0_73_and_185_kW


class F7_meets_installation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the installation meet the installation guidelines defined in' \
            ' Activity Definition F7?'

    def formula(buildings, period, parameters):
        is_installed = buildings('F7_motor_is_installed', period)
        between_0_73_and_185_kW = buildings('F7_output_between_0_73_and_185_kW', period)
        return (is_installed * between_0_73_and_185_kW)
