from wsgiref.validate import InputWrapper
import numpy as np
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from openfisca_core.variables import Variable
from openfisca_nsw_safeguard.regulation_reference import PDRS_2022, ESS_2021


class PDRS_AC_baseline_input_power(Variable):
    value_type = float
    entity = Building
    label = 'returns the baseline input power for an Air Conditioner'
    definition_period = ETERNITY
    metadata = {
        "alias": "Baseline Power Input",
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        cooling_capacity = buildings(
            'Air_Conditioner__cooling_capacity', period)
        baseline_AEER = buildings(
            'Air_Conditioner__baseline_AEER', period)
        return cooling_capacity / baseline_AEER


class PDRS_AC_baseline_peak_adjustment_factor(Variable):
    value_type = float
    entity = Building
    label = 'returns the baseline peak adjustment factor for an Air Conditioner'
    definition_period = ETERNITY
    metadata = {
        "alias": "Baseline Power Input",
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        climate_zone = buildings('BCA_climate_zone', period)
        temperature_factor = parameters(period).PDRS.table_A28_temperature_factor.temperature_factor[climate_zone]
        usage_factor = 0.72
        return temperature_factor / usage_factor



class Air_Conditioner__baseline_AEER(Variable):
    value_type = float
    entity = Building
    label = 'returns the baseline input power for an Air Conditioner'
    definition_period = ETERNITY
    metadata = {
        "alias": "Baseline Power Input",
        "regulation_reference": PDRS_2022["XX", "AC"]
    }

    def formula(buildings, period, parameters):
        product_class = buildings('Air_Conditioner_type', period)
        installation_type = buildings('Appliance__installation_type', period)
        install_or_replacement = installation_type.possible_values
        new_AC_cooling_capacity = buildings('new_AC_cooling_capacity', period)
        cooling_capacity = np.select(
                                    [ 
                                        new_AC_cooling_capacity < 4,
                                        ((new_AC_cooling_capacity >= 4) * (new_AC_cooling_capacity < 10)),
                                        ((new_AC_cooling_capacity >= 10) * (new_AC_cooling_capacity < 39)),
                                        ((new_AC_cooling_capacity >= 39) * (new_AC_cooling_capacity <= 65)),
                                        (new_AC_cooling_capacity > 65)
                                    ],
                                    [
                                        "less_than_4kW",
                                        "4kW_to_10kW",
                                        "10kW_to_39kW",
                                        "39kW_to_65kW",
                                        "more_than_65kW",
                                    ]
                                    )
        baseline_AEER = np.select([
                                    installation_type == install_or_replacement.install,
                                    installation_type == install_or_replacement.replacement,
                                    ],
                                    [
                                        parameters(period).PDRS.AC.table_D16_2['AEER'][product_class][cooling_capacity],
                                        parameters(period).PDRS.AC.table_D16_3['AEER'][product_class][cooling_capacity]
                                    ])
        return baseline_AEER


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


class PDRS_AC_input_power(Variable):
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

    def formula(buildings, period, parameters):

        baseline_power_input = buildings(
            'PDRS_AC_baseline_input_power', period)
        baseline_peak_adjustment_factor = buildings(
            'PDRS_AC_baseline_peak_adjustment_factor', period)
        input_power = buildings('PDRS_AC_input_power', period)
        peak_adjustment_factor = baseline_peak_adjustment_factor
        firmness_factor = parameters(period).PDRS.table_A6_firmness_factor.firmness_factor['HVAC1']

        return (
                    (
                        baseline_power_input *
                        baseline_peak_adjustment_factor
                    ) -
                    (
                        input_power *
                        peak_adjustment_factor
                    )
                    *
                    firmness_factor
            )