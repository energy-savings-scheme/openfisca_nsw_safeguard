import numpy as np
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_core.variables import Variable
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021


class PDRS_AC_baseline_power_input(Variable):
    value_type = float
    entity = Building
    label = 'returns the baseline power input for an Air Conditioner'
    definition_period = ETERNITY
    metadata = {
        "alias": "Baseline Power Input",
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(building, period, parameters):
        cooling_capacity = building(
            'Air_Conditioner__cooling_capacity', period)

        cooling_capacity_enum = building('AC_cooling_capacity_enum', period)
        AC_type = building('Air_Conditioner_type', period)
        replace_or_install = building('Appliance__installation_type', period)

        baseline_unit = parameters(
            period).PDRS.AC.AC_baseline_power_per_capacity_reference_table[replace_or_install]
        scale = baseline_unit[AC_type]

        return scale[cooling_capacity_enum]*cooling_capacity


class PDRS_AC_duration_factor(Variable):
    reference = 'computing duration factor during the peak hour usage as part of the firmness factor in PDRS Air Conditioner savings.'
    entity = Building
    value_type = float
    definition_period = ETERNITY
    metadata = {
        'alias': "Duration Factor",
        "regulation_reference": PDRS_2022["XX", "AC"]
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


class PDRS_AC_firmness_factor(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    metadata = {
        'alias': "PDRS AC Firmness Factor",
        "regulation_reference": PDRS_2022["XX", "AC"]
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
            'PDRS_AC_duration_factor', period)

        return contribution_factor*load_factor*duration_factor


class PDRS_AC_power_input(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the measured full capacity power input at 35C as recorded in the GEMS register?"
    metadata = {
        "alias": "AC power input",
        "regulation_reference": PDRS_2022["XX", "AC"]
    }


class PDRS_AC_peak_demand_savings(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The final peak demand savings from the air conditioner"
    metadata = {
        "alias": "AC Peak Demand Savings",
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(building, period, parameters):

        power_input = building('PDRS_AC_power_input', period)
        baseline_power_input = building(
            'PDRS_AC_baseline_power_input', period)
        firmness_factor = building(
            'PDRS_AC_firmness_factor', period)
        daily_peak_hours = parameters(
            period).PDRS.PDRS_wide_constants.DAILY_PEAK_WINDOW_HOURS
        forward_creation_period = parameters(
            period).PDRS.AC.AC_related_constants.FORWARD_CREATION_PERIOD

        diff = np.where((baseline_power_input - power_input) >
                        0, baseline_power_input - power_input, 0)

        return diff*daily_peak_hours*firmness_factor*forward_creation_period
