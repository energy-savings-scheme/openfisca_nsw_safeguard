import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021


class ESS_D16__Air_Conditioner__heating_capacity(Variable):
    reference = "unit in kw"
    value_type = float
    entity = Building
    label = "What is the product cooling capacity in the label?"
    definition_period = ETERNITY
    metadata = {
        "variable-type": "user-input",
        "alias": "Air Conditioner Cooling Capacity",
        "regulation_reference": ESS_2021["D", "D16"]
    }


class ESS_D16__Air_Conditioner__cooling_annual_energy_use(Variable):
    reference = "unit in kw"
    value_type = float
    entity = Building
    label = "What is the product cooling Energy Use on the Zoned Energy Rating Label?"
    definition_period = ETERNITY
    metadata = {
        "variable-type": "user-input",
        "alias": "Air Conditioner Cooling Annual Energy Use",
        "regulation_reference": ESS_2021["D", "D16"]
    }


class ESS_D16__Air_Conditioner__heating_annual_energy_use(Variable):
    reference = "unit in kw"
    value_type = float
    entity = Building
    label = "What is the product heating Energy Use on the Zoned Energy Rating Label?"
    definition_period = ETERNITY
    metadata = {
        "variable-type": "user-input",
        "alias": "Air Conditioner Heating Annual Energy Use",
        "regulation_reference": ESS_2021["D", "D16"]
    }


class ESS_D16__reference_cooling_energy_use(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The reference cooling annual energy use for the air conditioning equipment.."
    metadata = {"variable-type": "inter-interesting",
                "regulation_reference": ESS_2021["D", "D16"]
                }

    def formula(building, period, parameters):
        AC_cooling_capacity = building(
            'Air_Conditioner__cooling_capacity', period)
        climate_zone = building('Appliance__zone_type', period)
        equivalent_cooling_hours = parameters(
            period).ESS.ESS_D16.cooling_and_heating_hours['cooling_hours'][climate_zone]
        AC_type = building('Air_Conditioner_type', period)
        cooling_capacity = np.select(
                                    [ 
                                        AC_cooling_capacity < 4,
                                        ((AC_cooling_capacity >= 4) * (AC_cooling_capacity < 10)),
                                        ((AC_cooling_capacity >= 10) * (AC_cooling_capacity < 39)),
                                        ((AC_cooling_capacity >= 39) * (AC_cooling_capacity <= 65)),
                                        (AC_cooling_capacity > 65)
                                    ],
                                    [
                                        "less_than_4kW",
                                        "4kW_to_10kW",
                                        "10kW_to_39kW",
                                        "39kW_to_65kW",
                                        "more_than_65kW",
                                    ]
                                    )
        installation_type = building(
            'Appliance__installation_type', period)
        install_or_replacement = installation_type.possible_values
        baseline_AEER = np.select([
                                    installation_type == install_or_replacement.install,
                                    installation_type == install_or_replacement.replacement,
                                    ],
                                    [
                                    parameters(period).PDRS.AC.table_D16_2['AEER'][AC_type][cooling_capacity],
                                    parameters(period).PDRS.AC.table_D16_3['AEER'][AC_type][cooling_capacity]
                                    ])
        return (
                (
                    AC_cooling_capacity * 
                    equivalent_cooling_hours
                ) * 
                baseline_AEER
                )


class ESS_D16__reference_heating_energy_use(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The reference heating annual energy use for the air conditioning equipment.."
    metadata = {"variable-type": "inter-interesting",
                "regulation_reference": ESS_2021["D", "D16"]
                }

    def formula(building, period, parameters):
        AC_heating_capacity = building(
            'ESS_D16__Air_Conditioner__heating_capacity', period)
        climate_zone = building('Appliance__zone_type', period)
        heating_capacity = np.select(
            [
                AC_heating_capacity < 4,
                (AC_heating_capacity < 10) * (AC_heating_capacity >= 4),
                (AC_heating_capacity < 39) * (AC_heating_capacity >= 10),
                (AC_heating_capacity < 65) * (AC_heating_capacity >= 39),
                AC_heating_capacity > 65
            ],
            [
                'less_than_4kW',
                '4kW_to_10kW',
                '10kW_to_39kW',
                '39kW_to_65kW',
                'more_than_65kW'
            ])
        equivalent_heating_hours = parameters(
            period).ESS.ESS_D16.cooling_and_heating_hours['heating_hours'][climate_zone]
        AC_type = building('Air_Conditioner_type', period)
        installation_type = building(
            'Appliance__installation_type', period)
        install_or_replacement = installation_type.possible_values
        baseline_ACOP = np.select([
                                    installation_type == install_or_replacement.install,
                                    installation_type == install_or_replacement.replacement,
                                    ],
                                    [
                                    parameters(period).PDRS.AC.table_D16_2['ACOP'][AC_type][heating_capacity],
                                    parameters(period).PDRS.AC.table_D16_3['ACOP'][AC_type][heating_capacity]
                                    ])
        return ((AC_heating_capacity * equivalent_heating_hours) * baseline_ACOP)
