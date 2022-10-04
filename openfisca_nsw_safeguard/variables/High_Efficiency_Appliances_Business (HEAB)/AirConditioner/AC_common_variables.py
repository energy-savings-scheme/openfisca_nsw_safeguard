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
    metadata = {
        'display_question': "Does the new air conditioner have a cooling capacity recorded in the GEMS registry?"
    }


class new_AC_heating_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the heating capacity for the new Air Conditioner?'
    metadata = {
        'display_question': "Does the new or replacement End-User equipment have a heating capacity recorded in the GEMS Registry?"
    }


class HVAC2_heating_capacity_input(Variable):
    # This is the variable for the data input from the GEMS Registry
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The HVAC2 heating capacity that pulls in from the GEMS Registry'
    metadata = {
        'variable-type': 'user-input'
    }


class HVAC2_equivalent_heating_hours_input(Variable):
    # This is the variable for the data input from the ESS Table F4.1
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The equivalent heating hours that pull in from Table F4.1'
    metadata = {
        'variable-type': 'user-input'
    }


class HVAC2_rated_ACOP_input(Variable):
    # This is the variable for the data input from the GEMS Registry
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The ACOP rating that pulls in from the GEMS Registry'
    metadata = {
        'variable-type': 'user-input'
    }


class HVAC2_baseline_ACOP_input(Variable):
    #This is the variable for the data input from the GEMS Registry
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The baseline ACOP rating that pulls in from the GEMS Registry'
    metadata = {
         'variable-type': 'user-input'
    }


class new_AC_EER(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the EER for the new AC?' 
    # Liam note: check to see how EER is calced \
    # across CC ACs and regular, <65kW ACs


class HVAC2_baseline_AEER_input(Variable):
    #This is the variable for the data input from the GEMS Registry
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The baseline AEER rating that pulls in from the GEMS Registry'
    metadata = {
         'variable-type': 'user-input'
    }


class HVAC2_cooling_capacity_input(Variable):
    # This is the variable for the data input from the GEMS Registry
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The HVAC2 cooling capacity that pulls in from the GEMS Registry'
    metadata = {
        'variable-type': 'user-input'
    }


class HVAC2_equivalent_cooling_hours_input(Variable):
    # This is the variable for the data input from the ESS Table F4.1
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The equivalent cooling hours that pull in from Table F4.1'
    metadata = {
        'variable-type': 'user-input'
}


class HVAC2_rated_AEER_input(Variable):
    # This is the variable for the data input from the GEMS Registry
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The AEER rating that pulls in from the GEMS Registry'
    metadata = {
        'variable-type': 'user-input'
    }


class HVAC2_lifetime_value(Variable):
    # This is the variable for the data input from ESS related constants
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The lifetime value that pulls in from related constants (Table D16)'
    metadata = {
        'variable-type': 'user-input'   
    }


class HVAC2_electricity_conversion_factor(Variable):
    # This is the variable for the data input from ESS certificate conversion factors
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The electricity conversion factor that pulls in from ESS certificate conversion factors'
    metadata = {
        'variable-type': 'user-input'   
    }