from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY, YEAR
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

import numpy as np
from datetime import date



class start_date_of_measurement_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'Start date of measurement period'


class end_date_of_measurement_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'End date of measurement period'


class measurement_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'Length of measurement period.'


class start_date_of_operating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'Start date of measurement period'


class end_date_of_operating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'End date of measurement period'


class operating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'Length of measurement period.'


class operating_period_is_valid(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Length of measurement period.'


class implementation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the implementation date of the implementation?'


class implementation_date_is_within_measurement_period(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Implementation Date within the measurement period?'

    def formula(buildings, period, parameters):
        measurement_period_start_date = buildings('start_date_of_measurement_period', period)
        measurement_period_end_date = buildings('end_date_of_measurement_period', period)
        implementation_date = buildings('implementation_date', period)
        implementation_date_after_start_of_measurement = (
            implementation_date > measurement_period_start_date
        )
        implementation_date_before_end_of_measurement = (
            implementation_date < measurement_period_end_date
        )
        return(
            implementation_date_after_start_of_measurement *
            implementation_date_before_end_of_measurement
        )
