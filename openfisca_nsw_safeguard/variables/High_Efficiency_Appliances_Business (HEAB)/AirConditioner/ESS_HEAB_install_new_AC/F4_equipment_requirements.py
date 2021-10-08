from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class is_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product registered in GEMS?'
    # a way you could operationalise this - link in w. GEMS Registry and see if \
    # the product is registered based on user input. You could also pull a \
    # dropdown from said Registry in the form of an Enum?


class F4_complies_with_GEMS_2019_AC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product comply with the Greenhouse and Energy Minimum' \
            ' Standards (Air Conditioners up to 65kW) Determination 2019?'
    # what does complying with this Determination mean?


class F4_complies_with_GEMS_2013_AC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product comply with the Greenhouse and Energy Minimum' \
            ' Standards (Air Conditioners and Heat Pumps) Determination 2013?'
    # what does complying with this Determination mean?


class F4_warranty_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the warranty length for the new air conditioner, in years?'


class F4_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the showerhead has a minimum warranty length of' \
            ' 5 years, as required by Equipment Requirement 2.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('F4_warranty_length', period)
        return warranty_length >= 5


class F4_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F4?'

    def formula(buildings, period, parameters):
        registered_in_GEMS = buildings('is_registered_in_GEMS', period)
        complies_with_GEMS_2019 = buildings('complies_with_GEMS_2019_AC', period)
        complies_with_GEMS_2013 = buildings('complies_with_GEMS_2013_AC', period)
        minimum_warranty_length = buildings('F4_minimum_warranty_length', period)
        return (registered_in_GEMS * (complies_with_GEMS_2019 + complies_with_GEMS_2013)
        * minimum_warranty_length)
