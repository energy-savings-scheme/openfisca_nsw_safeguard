from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class new_AC_reference_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the reference cooling annual energy use for the new air conditioner?'

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('cooling_capacity', period)
        weather_zone = buildings('weather_zone', period)
        cooling_hours = parameters(period).HEAB.ESS_HEAB_install_new_AC.cooling_and_heating_hours.cooling_hours[weather_zone]
        product_class = buildings('ESS_HEAB_install_new_AC_product_class', period)
        baseline_cooling_AEER = parameters(period).HEAB.ESS_HEAB_install_new_AC.baseline_AEER_and_ACOP.AEER[product_class]
        return cooling_capacity * cooling_hours / baseline_cooling_AEER


class new_AC_cooling_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the cooling capacity for the new Air Conditioner?'


class new_AC_heating_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the heating capacity for the new Air Conditioner?'


class new_AC_EER(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the EER for the new AC?' 
    #TODO - check to see how EER is calced \
    # across CC ACs and regular, <65kW ACs
 