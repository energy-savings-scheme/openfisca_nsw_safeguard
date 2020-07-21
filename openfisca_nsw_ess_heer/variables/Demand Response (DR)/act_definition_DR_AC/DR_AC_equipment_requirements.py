# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class DR_AC_is_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product registered in GEMS?'
    # a way you could operationalise this - link in w. GEMS Registry and see if \
    # the product is registered based on user input. You could also pull a \
    # dropdown from said Registry in the form of an Enum?


class DR_AC_complies_with_GEMS_2019_AC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product comply with the Greenhouse and Energy Minimum' \
            ' Standards (Air Conditioners up to 65kW) Determination 2019?'
    # what does complying with this Determination mean?


class DR_AC_complies_with_GEMS_2013_AC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product comply with the Greenhouse and Energy Minimum' \
            ' Standards (Air Conditioners and Heat Pumps) Determination 2013?'
    # what does complying with this Determination mean?


class DR_AC_complies_with_AS_4755_3_1(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product comply with AS4755.3.1?'
    # what does complying with this Standard mean?


class DR_AC_complies_with_AS_4755_2(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product comply with AS4755.2?'
    # what does complying with this Standard mean?


class DR_AC_is_capable_of_DRM1(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the AC capable of demand response mode DRM1?'


class DR_AC_is_capable_of_DRM2(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the AC capable of demand response mode DRM2?'
    # what does complying with this Standard mean?


class DR_AC_is_capable_of_DRM3(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the AC capable of demand response mode DRM3?'
    # what does complying with this Standard mean?


class DR_AC_warranty_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the warranty length for the new air conditioner, in years?'


class DR_AC_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the showerhead has a minimum warranty length of' \
            ' 5 years, as required by Equipment Requirement 2.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('DR_AC_warranty_length', period)
        return warranty_length >= 5


class DR_AC_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F4?'

    def formula(buildings, period, parameters):
        registered_in_GEMS = buildings('is_registered_in_GEMS', period)
        complies_with_GEMS_2019 = buildings('complies_with_GEMS_2019_AC', period)
        complies_with_GEMS_2013 = buildings('complies_with_GEMS_2013_AC', period)
        complies_with_AS_4755_3_1 = buildings('DR_AC_complies_with_AS_4755_3_1', period)
        complies_with_AS_4755_2 = buildings('DR_AC_complies_with_AS_4755_2', period)
        capable_of_DRM1 = buildings('DR_AC_is_capable_of_DRM1', period)
        capable_of_DRM2 = buildings('DR_AC_is_capable_of_DRM2', period)
        capable_of_DRM3 = buildings('DR_AC_is_capable_of_DRM3', period)
        minimum_warranty_length = buildings('F4_minimum_warranty_length', period)
        return (registered_in_GEMS
        * (complies_with_GEMS_2019 + complies_with_GEMS_2013)
        * (complies_with_AS_4755_3_1 + complies_with_AS_4755_2)
        * (capable_of_DRM1 + capable_of_DRM2 + capable_of_DRM3)
        * minimum_warranty_length)
