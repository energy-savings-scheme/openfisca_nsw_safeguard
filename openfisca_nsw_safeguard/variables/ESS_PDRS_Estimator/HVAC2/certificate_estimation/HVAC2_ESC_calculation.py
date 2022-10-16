from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class HVAC2_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual heating energy use'
    metadata = {
        "alias": "Annual heating energy use",
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      heating_capacity = buildings('HVAC2_heating_capacity_input', period)
      equivalent_heating_hours = buildings('HVAC2_equivalent_heating_hours_input', period)
      rated_ACOP = buildings('HVAC2_rated_ACOP_input', period)

      annual_heating = np.floor(heating_capacity * equivalent_heating_hours) / rated_ACOP
      return annual_heating


class HVAC2_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Annual cooling energy use'
    metadata = {
        "alias": "Annual cooling energy use",
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      cooling_capacity = buildings('HVAC2_cooling_capacity_input', period)
      equivalent_cooling_hours = buildings('HVAC2_equivalent_cooling_hours_input', period)
      rated_AEER = buildings('HVAC2_rated_AEER_input', period)

      annual_cooling = np.floor(cooling_capacity * equivalent_cooling_hours) / rated_AEER
      return annual_cooling


class HVAC2_reference_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Reference annual heating energy use'
    metadata = {
        "alias": "Reference annual heating energy use",
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      heating_capacity = buildings('HVAC2_heating_capacity_input', period)
      equivalent_heating_hours = buildings('HVAC2_equivalent_heating_hours_input', period)
      baseline_ACOP = buildings('HVAC2_baseline_ACOP_input', period)
      
      reference_annual_heating = np.floor(heating_capacity * equivalent_heating_hours) / baseline_ACOP
      return reference_annual_heating

  
class HVAC2_reference_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Reference annual cooling energy use'
    metadata = {
        "alias": "Reference annual cooling energy use",
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      cooling_capacity = buildings('HVAC2_cooling_capacity_input', period)
      equivalent_cooling_hours = buildings('HVAC2_equivalent_cooling_hours_input', period)
      baseline_AEER = buildings('HVAC2_baseline_AEER_input', period)

      reference_annual_cooling = np.floor(cooling_capacity * equivalent_cooling_hours) / baseline_AEER
      return reference_annual_cooling


class HVAC2_deemed_activity_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Deemed activity electricity savings'
    metadata = {
        "alias": "Deemed activity electricity savings",
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      reference_annual_cooling = buildings('HVAC2_reference_cooling_annual_energy_use', period)
      annual_cooling = buildings('HVAC2_cooling_annual_energy_use', period)
      reference_annual_heating = buildings('HVAC2_reference_heating_annual_energy_use', period)
      annual_heating = buildings('HVAC2_heating_annual_energy_use', period)
      lifetime = buildings('HVAC2_lifetime_value', period)

      deemed_electricity_savings = (reference_annual_cooling - annual_cooling) + (reference_annual_heating - annual_heating) * (lifetime / 1000)
      return deemed_electricity_savings


class HVAC2_PDRS__regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"PDRS Regional Network Factor",
        "display_question": "PDRS regional network factor",
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        postcode = buildings('PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided


class HVAC2_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'HVAC2 Electricity savings'
    metadata = {
        "alias": "HVAC2 electricity savings",
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
        deemed_electricity_savings = buildings('HVAC2_deemed_activity_electricity_savings', period)   
        regional_network_factor = buildings('HVAC2_PDRS__regional_network_factor', period)

        HVAC2_electricity_savings = np.floor(deemed_electricity_savings * regional_network_factor)
        return HVAC2_electricity_savings


class HVAC2_ESC_calculation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'The number of ESCs for HVAC2'
    metadata = {
        "variable-type": "output"
    }

    def formula(buildings, period, parameters):
      HVAC2_electricity_savings = buildings('HVAC2_electricity_savings', period)
      electricity_certificate_conversion_factor = 1.06

      HVAC2_ESC_calculation = np.floor(HVAC2_electricity_savings * electricity_certificate_conversion_factor)

      return HVAC2_ESC_calculation
