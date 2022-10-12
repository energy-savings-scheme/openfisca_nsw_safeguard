import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Building
from datetime import date


class Base_reduces_energy_consumption(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Does the activity reduce energy consumption?'
    metadata = {
        'display_question' : 'Does your activity reduce energy consumption compared to what would have been consumed?',
        'sorting' : 1
    }


class Base_provides_capacity_to_reduce_demand(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Does the activity provide the capacity to reduce demand?'
    metadata = {
        'display_question': 'Does your activity provide capacity to reduce demand during the Peak Demand Reduction period?',
        'sorting' : 2
    }


class Base_implemented_activity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Has implementation already occurred?'
    metadata = {
        'display_question' : 'Has your implementation already occurred?',
        'sorting' : 3
    }


class Base_implementation_after_1_April_2022(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What date did the implementation occur?'
    metadata = {
        'display_question' : 'What date did the implementation occur?',
        'sorting' : 4
    }


class Base_lawful_activity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label ='Was your activity lawful in NSW on the implementation date?'
    metadata = {
        'display_question' : 'Was your activity lawful in NSW on the implementation date?',
        'sorting' : 5
    }


class Base_registered_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Are you an ACP?'
    metadata = {
        'display_question' : 'Are you an ACP?',
        'sorting' : 6
    }


class Base_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Did you engage an Accredited Certificate Provider prior to the implementation date?'
    metadata = {
        'display_question' : 'Did you engage an Accredited Certificate Provider prior to the implementation date?',
        'sorting' : 7,
        'conditional': 'True'
    }


class Base_removing_or_replacing(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Are you removing or replacing End-User equipment?'
    metadata = {
        'display_question' : 'Are you removing or replacing End-User equipment?',
        'sorting' : 8
    }


class Base_not_resold_reused_or_refurbished(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is the removed End-User equipment re-sold, refurbished or re-used?'
    metadata = {
        'display_question' : 'Is the removed End-User equipment re-sold, refurbished or re-used?',
        'sorting' : 9,
        'conditional': 'True'
    }


class Base_disposal_of_equipment(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Will your End-User equipment be disposed of in accordance with legal requirements, (including by obtaining evidence for any refrigerants being disposed of or recycled)?'
    metadata = {
        'display_question' : 'Will your End-User equipment be disposed of in accordance with legal requirements, (including by obtaining evidence for any refrigerants being disposed of or recycled)?',
        'sorting' : 10,
        'conditional': 'True'
    }


class Base_reduces_safety_levels(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Will your activity reduce safety levels or permanently reduce production or service levels?'
    metadata = {
        'display_question' : 'Will your activity reduce safety levels or permanently reduce production or service levels?',
        'sorting' : 11
    }


class Base_greenhouse_emissions_increase(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Will your activity lead to a net increase in greenhouse emissions?'
    metadata = {
        'display_question': 'Will your activity lead to a net increase in greenhouse emissions?',
        'sorting' : 12
    }


class Base_meets_mandatory_requirement(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is your activity being undertaken to comply with any mandatory legal requirements?'
    metadata = {
        'display_question': 'Is your activity being undertaken to comply with any mandatory legal requirements?',
        'sorting' : 13,
        'conditional': 'True'
    }


class Base_basix_affected_development(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is your activity an alteration, enlargement or extension of a BASIX affected development?'
    metadata = {
        'display_question': 'Is your activity an alteration, enlargement or extension of a BASIX affected development?',
        'sorting' : 14
    }


class Base_prescribed_transmission_service(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Is your activity a Standard Control Service or Prescribed Transmission service undertaken by a Network Service Provider?'
    metadata = {
        'display_question': 'Is your activity a Standard Control Service or Prescribed Transmission service undertaken by a Network Service Provider?',
        'sorting' : 15
    }


class Base_tradeable_certificates(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Have you created tradeable certificates under the Renewable Energy Act?'
    metadata = {
        'display_question' : 'Have you created tradeable certificates under the Renewable Energy Act?',
        'sorting' : 16
    }


class Base_replacement_water_heater_certificates(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is the activity the installation of a replacement heat pump water heater?'
    metadata = {
        'display_question' : 'Is the activity the installation of a replacement heat pump water heater?',
        'sorting' : 17,
        'conditional': 'True'
    }


class Base_replacement_solar_water_heater_certificates(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Is the activity the installation of a replacement solar water heater?'
    metadata = {
        'display_question' : 'Is the activity the installation of a replacement solar water heater?',
        'sorting' : 18,
        'conditional': 'True'
    }