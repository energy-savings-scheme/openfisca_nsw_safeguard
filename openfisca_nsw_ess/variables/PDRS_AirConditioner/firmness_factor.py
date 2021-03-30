from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class PDRS__Air_Conditioner__duration_factor(Variable):
    reference='computing duration factor during the peak hour usage as part of the firmness factor in PDRS Air Conditioner savings.'
    entity=Building
    value_type=float
    definition_period=ETERNITY
    metadata ={
        'alias' : "Duration Factor",
        'activity-group' : "Air Conditioners?",
        'activity-name' : "Replace or Install an Air Conditioner",
        'variable-type' : "intermediary"
    }

    def formula(building, period, parameters):
        installation_purpose=building('PDRS__Appliance__installation_purpose', period)
        zone_type = building('PDRS__Appliance__zone_type', period)
        operation_hrs = parameters(period).PDRS.AC.hours_of_operation_by_zone_table[zone_type]
        ratio = parameters(period).PDRS.AC.peak_operation_hrs_to_all_operation_hrs_by_zone_table[zone_type]
        weekdays_ratio = float(5/7)
        peak_hours = parameters(period).PDRS.AC.related_constants.ANNUAL_PEAK_WINDOW_HOURS


        return operation_hrs[installation_purpose]*ratio[installation_purpose]*weekdays_ratio/peak_hours


class PDRS__Air_Conditioner__firmness_factor(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    metadata ={
        'alias' : "Firmness Factor",
        'activity-group' : "Air Conditioners?",
        'activity-name' : "Replace or Install an Air Conditioner",
        'variable-type' : "intermediary"
    }

    def formula(building, period, parameters):
        installation_purpose=building('PDRS__Appliance__installation_purpose', period)
        zone_type = building('PDRS__Appliance__zone_type', period)
        load_factor = parameters(period).PDRS.AC.load_factors_table[installation_purpose]
        contribution_factor = parameters(period).PDRS.AC.related_constants.CONTRIBUTION_FACTOR
        duration_factor=building('PDRS__Air_Conditioner__duration_factor', period)

        return contribution_factor*load_factor*duration_factor