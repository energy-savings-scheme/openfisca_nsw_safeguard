from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

class PDRS__Air_Conditioner__duration_factor(Variable):
    reference = 'computing duration factor during the peak hour usage as part of the firmness factor in PDRS Air Conditioner savings.'
    entity = Building
    value_type = float
    definition_period = ETERNITY
    metadata = {
        'alias': "Duration Factor",
        # 'activity-group': "Air Conditioners?",
        # 'activity-name': "Replace or Install an Air Conditioner",
        'variable-type': "intermediary",
        # "activity-group": "PDRS: Air Conditioner",
        # "activity-name": "Installation or Replacement of an Air Conditioner"
        "regulation_reference": PDRS_2022["8","5"]
    }

    def formula(building, period, parameters):
        installation_purpose = building(
            'Appliance__installation_purpose', period)
        zone_type = building('Appliance__zone_type', period)
        operation_hrs = parameters(
            period).PDRS.AC.AC_hours_of_operation_by_zone_table[zone_type]
        ratio = parameters(
            period).PDRS.AC.AC_peak_operation_hrs_to_all_operation_hrs_by_zone_table[zone_type]
        weekdays_ratio = float(5/7)
        peak_hours = parameters(
            period).PDRS.PDRS_wide_constants.ANNUAL_PEAK_WINDOW_HOURS

        return operation_hrs[installation_purpose]*ratio[installation_purpose]*weekdays_ratio/peak_hours


class PDRS__Air_Conditioner__firmness_factor(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    metadata = {
        'alias': "Firmness Factor",
        # 'activity-group': "Air Conditioners?",
        # 'activity-name': "Replace or Install an Air Conditioner",
        'variable-type': "intermediary",
        "regulation_reference": PDRS_2022["8","5"]
    }

    def formula(building, period, parameters):
        installation_purpose = building(
            'Appliance__installation_purpose', period)
        zone_type = building('Appliance__zone_type', period)
        load_factor = parameters(
            period).PDRS.AC.AC_load_factors_table[installation_purpose]
        contribution_factor = parameters(
            period).PDRS.PDRS_wide_constants.CONTRIBUTION_FACTOR
        duration_factor = building(
            'PDRS__Air_Conditioner__duration_factor', period)

        return contribution_factor*load_factor*duration_factor
