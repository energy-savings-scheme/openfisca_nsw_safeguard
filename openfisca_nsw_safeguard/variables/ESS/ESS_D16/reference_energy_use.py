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
        # "major-cat": "Energy Savings Scheme",
        # "monor-cat": "Installation or Replacement of an Air Conditioner",
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
        # "major-cat": "Energy Savings Scheme",
        # "monor-cat": "Installation or Replacement of an Air Conditioner",
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
        # "major-cat": "Energy Savings Scheme",
        # "monor-cat": "Installation or Replacement of an Air Conditioner",
        "regulation_reference": ESS_2021["D", "D16"]
    }


class AC_heating_capacity(Enum):
    less_than_4 = "heating capacity < 4kW"
    between_4_and_10 = "4kw =< heating capacity < 10kW"
    between_10_and_39 = "10kw =< heating capacity < 39kW"
    between_39_and_65 = "39kw =< heating capacity < 65kW"
    more_than_65 = "heating capacity >= 65kW"


class ESS_D16__reference_cooling_energy_use(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The reference cooling annual energy use for the air conditioning equipment.."
    metadata = {"variable-type": "inter-interesting",         
                # "major-cat": "Energy Savings Scheme",
                # "monor-cat": "Installation or Replacement of an Air Conditioner",
                "regulation_reference": ESS_2021["D", "D16"]
                }

    def formula(building, period, parameters):
        cooling_capacity = building(
            'Air_Conditioner__cooling_capacity', period)
        climate_zone = building('Appliance__zone_type', period)
        cooling_capacity_enum = building('AC_cooling_capacity_enum', period)
        equivalent_cooling_hours = parameters(
            period).ESS.ESS_D16.cooling_and_heating_hours['cooling_hours'][climate_zone]
        AC_type = building('Air_Conditioner_type', period)
        installation_type = building(
            'Appliance__installation_type', period)
        AEER = parameters(
            period).ESS.ESS_D16.baseline_AEER_and_ACOP['AEER'][installation_type][AC_type][cooling_capacity_enum]
        return ((cooling_capacity * equivalent_cooling_hours) * AEER)


class ESS_D16__reference_heating_energy_use(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The reference heating annual energy use for the air conditioning equipment.."
    metadata = {"variable-type": "inter-interesting",         
                # "major-cat": "Energy Savings Scheme",
                # "monor-cat": "Installation or Replacement of an Air Conditioner",
                "regulation_reference": ESS_2021["D", "D16"]
                }

    def formula(building, period, parameters):
        heating_capacity = building(
            'ESS_D16__Air_Conditioner__heating_capacity', period)
        climate_zone = building('Appliance__zone_type', period)
        heating_capacity_enum = np.select(
            [
                heating_capacity < 4,
                (heating_capacity < 10) * (heating_capacity >= 4),
                (heating_capacity < 39) * (heating_capacity >= 10),
                (heating_capacity < 65) * (heating_capacity >= 39),
                heating_capacity > 65
            ],
            [
                AC_heating_capacity.less_than_4,
                AC_heating_capacity.between_4_and_10,
                AC_heating_capacity.between_10_and_39,
                AC_heating_capacity.between_39_and_65,
                AC_heating_capacity.more_than_65
            ])
        equivalent_heating_hours = parameters(
            period).ESS.ESS_D16.cooling_and_heating_hours['heating_hours'][climate_zone]
        AC_type = building('Air_Conditioner_type', period)
        installation_type = building(
            'Appliance__installation_type', period)
        AEER = parameters(
            period).ESS.ESS_D16.baseline_AEER_and_ACOP['ACOP'][installation_type][AC_type][heating_capacity_enum]
        return ((heating_capacity * equivalent_heating_hours) * AEER)
