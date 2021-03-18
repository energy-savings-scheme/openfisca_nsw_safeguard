from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


# Where to put global constants ? Do they need to be displayed?


class zone_type(Enum):
    hot="Hot"
    average="Average"
    cold="Cold"

class PDRS__Appliance__zone_type(Variable):
    entity=Building
    value_type=Enum
    possible_values=zone_type
    default_value=zone_type.average
    definition_period=ETERNITY
    reference="Clause **"
    label="What is the Zone type of the area?" 


class installation_purpose(Enum):
    residential='Residential/SME'
    commercial='Commercial'


class PDRS__Appliance__installation_purpose(Variable):
    entity=Building
    value_type=Enum
    possible_values=installation_purpose
    default_value=installation_purpose.residential
    definition_period=ETERNITY
    reference="Clause **"
    label="Is the air-conditioner(s) installed for Residential or Commercial purpose?" #wording as form input. 



class PDRS__Air_Conditioner__duration_factor(Variable):
    reference='computing duration factor during the peak hour usage as part of the firmness factor in PDRS Air Conditioner savings.'
    entity=Building
    value_type=float
    definition_period=ETERNITY

    def formula(building, period, parameters):
        installation_purpose=building('PDRS__Appliance__installation_purpose', period)
        zone_type = building('PDRS__Appliance__zone_type', period)
        operation_hrs = parameters(period).AC_hours_of_operation_by_zone_table[zone_type]
        ratio = parameters(period).AC_peak_operation_hrs_to_all_operation_hrs_by_zone_table[zone_type]
        weekdays_ratio = float(5/7)
        peak_hours = parameters(period).AC_related_constants.NUMBER_OF_PEAK_WINDOW_HOURS


        return operation_hrs[installation_purpose]*ratio[installation_purpose]*weekdays_ratio/peak_hours


class PDRS__Air_Conditioner__firmness_factor(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY

    def formula(building, period, parameters):
        installation_purpose=building('PDRS__Appliance__installation_purpose', period)
        zone_type = building('PDRS__Appliance__zone_type', period)
        load_factor = parameters(period).AC_load_factors_table[installation_purpose]
        contribution_factor = parameters(period).AC_related_constants.CONTRIBUTION_FACTOR
        ## call the duration factor computed from above? How to call the formula under PDRS__Air_Conditioner__duration_factor ?
        duration_factor=building('PDRS__Air_Conditioner__duration_factor', period)

        return contribution_factor*load_factor*duration_factor