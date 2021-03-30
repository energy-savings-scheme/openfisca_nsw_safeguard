from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS__D16__deemed_elec_savings(Variable):
    entity=Building
    value_type=float
    definition_period=ETERNITY
    reference="Clause **"
    label="The final deemed electricity savings for installing a high efficiency AC."
    metadata={"variable-type":"final_output"}

    def formula(building, period, parameters):
        reference_cooling_energy_use = building('ESS_D16__reference_cooling_energy_use', period)
        cooling_energy_use = building('ESS_D16__Air_Conditioner__cooling_annual_energy_use', period)
        reference_heating_energy_use = building('ESS_D16__reference_heating_energy_use', period)
        heating_energy_use = building('ESS_D16__Air_Conditioner__heating_annual_energy_use', period)
        lifetime = parameters(period).D16_related_constants.LIFETIME
        MWh_to_kWh = parameters(period).ESS_related_constants.MWh_to_kWh # note that formula requires dividing by 1000
                                                                         # * by 0.001 is better, as end unit is MWh
        return (((reference_cooling_energy_use - cooling_energy_use) + (reference_heating_energy_use - heating_energy_use)) * lifetime / MWh_to_kWh)
