# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F3_is_close_control_air_conditioner(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product a close control air conditioner?'


class F3_is_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product registered in GEMS?'
    # a way you could operationalise this - link in w. GEMS Registry and see if \
    # the product is registered based on user input. You could also pull a \
    # dropdown from said Registry in the form of an Enum?


class F3_complies_with_GEMS_2012_CCAC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product comply with the Greenhouse and Energy Minimum' \
            ' Standards (Close Control Air Conditioner) Determination 2012?'
    # what does complying with this Determination mean?


class F3_EER_20_percent_higher_than_baseline(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product have an EER at least 20% higher than the' \
            ' baseline for the corresponding type and cooling capacity,' \
            ' detailed in Table F3.1?'
    # what does complying with this Determination mean?

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('F3_CCAC_cooling_capacity', period)
        EER = buildings('F3_EER', period)
        capacity = select([cooling_capacity < 19.05,
                           cooling_capacity >= 19.05 and cooling_capacity < 39.5,
                           cooling_capacity >= 39.5 and cooling_capacity < 70.0,
                           cooling_capacity >= 70.0],
                          ['less_than_19_05_kW',
                           '19_05_kW_to_39_50_kW',
                           '39_50_kW_to_70_kW',
                           'more_than_70_kW'])
        baseline = parameters(period).HEAB.F3.F3_1[capacity]
        percentage_increase = ((EER - baseline) * 100)  # i'm sure there's a more efficient way to write this
        return percentage_increase > 20


class F3_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F4?'

    def formula(buildings, period, parameters):
        is_CCAC = buildings('F3_is_close_control_air_conditioner', period)
        registered_in_GEMS = buildings('F3_is_registered_in_GEMS', period)
        complies_with_GEMS_2012 = buildings('F3_complies_with_GEMS_2012_CCAC', period)
        EER_higher_than_baseline = buildings('F3_EER_20_percent_higher_than_baseline', period)
        return (is_CCAC * registered_in_GEMS * complies_with_GEMS_2012 * EER_higher_than_baseline)
