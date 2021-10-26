
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np
import time
import datetime
from datetime import date

# note because this activity definition requires calculation based off years, \
# you need to import the above libraries to make it work

epoch = time.gmtime(0).tm_year
today_date_and_time = np.datetime64(datetime.datetime.now())
today = today_date_and_time.astype('datetime64[D]')

# variables used to calculate age of equipment.


class ESS_HEAB_existing_equipment_installation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the installation date for the existing equipment?'


class ESS_HEAB_existing_equipment_age(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the age of the existing equipment, in years?'

    def formula(buildings, period, parameters):
        existing_equipment_installation_date = buildings('ESS_HEAB_existing_equipment_installation_date', period)
        existing_equipment_age_in_days = ((today.astype('datetime64[D]') - existing_equipment_installation_date.astype('datetime64[D]')).astype('datetime64[D]'))
        existing_equipment_age_in_years = existing_equipment_age_in_days.astype('datetime64[Y]')
        existing_equipment_age_as_int = (existing_equipment_age_in_years).astype('int')
        return (existing_equipment_age_as_int)