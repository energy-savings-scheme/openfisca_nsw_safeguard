from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

class ESS_D16__cooling_power_input(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the measured cooling power input at 35C as recorded in the GEMS register?"
    metadata = {
                "alias": "Air Conditioner Cooling Input Power",
                "variable-type": "user_input", 
                "regulation_reference": ESS_2021["D", "D16"]
                }


class ESS_D16__heating_power_input(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "What is the measured cooling power input at 35C as recorded in the GEMS register?"
    metadata = {
                "alias": "Air Conditioner Heating Input Power",
                "variable-type": "user_input", 
                "regulation_reference": ESS_2021["D", "D16"]
                }


class ESS_D16__cooling_annual_energy_use(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The cooling annual energy use for the air conditioning equipment."
    metadata = {
                "alias": "Air Conditioner Cooling Annual Energy Use",
                "variable-type": "inter-interesting", 
                "regulation_reference": ESS_2021["D", "D16"]
                }

    def formula(building, period, parameters):
        cooling_power_input = building('ESS_D16__cooling_power_input', period)
        zone_type = building('Appliance__zone_type', period)
        equivalent_cooling_hours = parameters(
            period).ESS.ESS_D16.cooling_and_heating_hours['cooling_hours'][zone_type]
        return cooling_power_input * equivalent_cooling_hours


class ESS_D16__heating_annual_energy_use(Variable):
    entity = Building
    value_type = float
    definition_period = ETERNITY
    reference = "Clause **"
    label = "The heating annual energy use for the air conditioning equipment."
    metadata = {
                "alias": "Air Conditioner Heating Annual Energy Use",
                "variable-type": "inter-interesting", 
                "regulation_reference": ESS_2021["D", "D16"]
                }

    def formula(building, period, parameters):
        heating_power_input = building('ESS_D16__heating_power_input', period)
        zone_type = building('Appliance__zone_type', period)
        equivalent_heating_hours = parameters(
            period).ESS.ESS_D16.cooling_and_heating_hours['heating_hours'][zone_type]
        return heating_power_input * equivalent_heating_hours
