# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class DR_AC_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F4?'

    def formula(buildings, period, parameters):
        reference_cooling_annual_energy_use = buildings('DR_AC_reference_cooling_annual_energy_use', period)
        cooling_annual_energy_use = buildings('DR_AC_cooling_annual_energy_use', period)
        reference_heating_annual_energy_use = buildings('DR_AC_reference_heating_annual_energy_use', period)
        heating_annual_energy_use = buildings('DR_AC_heating_annual_energy_use', period)
        lifetime = parameters(period).HEAB.F4.lifetime
        MWh_conversion = parameters(period).general_ESS.MWh_conversion
        return (((reference_cooling_annual_energy_use - cooling_annual_energy_use)
        + (reference_heating_annual_energy_use - heating_annual_energy_use)) * lifetime / MWh_conversion)


class DR_AC_reference_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the reference cooling annual energy use for the AC, as' \
            ' defined in Table F4.4?'

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('DR_AC_cooling_capacity', period)
        weather_zone = buildings('weather_zone', period)
        cooling_hours = parameters(period).HEAB.F4.cooling_and_heating_hours.cooling_hours[weather_zone]
        product_class = buildings('DR_AC_product_class', period)
        baseline_cooling_AEER = parameters(period).HEAB.F4.baseline_AEER_and_ACOP.AEER[product_class]
        return cooling_capacity * cooling_hours / baseline_cooling_AEER


class DR_AC_cooling_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the cooling capacity for Activity Definition F4?'


class DR_AC_reference_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the reference heating annual energy use for the AC, as' \
            ' defined in Table F4.4?'

    def formula(buildings, period, parameters):
        heating_capacity = buildings('heating_capacity', period)
        weather_zone = buildings('weather_zone', period)
        heating_hours = parameters(period).HEAB.F4.cooling_and_heating_hours.heating_hours[weather_zone]
        product_class = buildings('DR_AC_product_class', period)
        baseline_heating_ACOP = parameters(period).HEAB.F4.baseline_AEER_and_ACOP.ACOP[product_class]
        return heating_capacity * heating_hours / baseline_heating_ACOP


class DR_AC_heating_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the heating capacity for Activity Definition F4?'


class DR_AC_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the cooling annual energy use for the AC, as defined in' \
            ' Table F4.4?'

    def formula(buildings, period, parameters):
        cooling_power_input = buildings('cooling_power_input', period)
        weather_zone = buildings('weather_zone', period)
        cooling_hours = parameters(period).HEAB.F4.cooling_and_heating_hours.cooling_hours[weather_zone]
        cooling_annual_energy_use = cooling_power_input * cooling_hours
        return cooling_annual_energy_use


class DR_AC_cooling_power_input(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the cooling power input for Activity Definition F4?'


class DR_AC_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the heating annual energy use for the AC, as defined in' \
            ' Table F4.4?'

    def formula(buildings, period, parameters):
        heating_power_input = buildings('heating_power_input', period)
        weather_zone = buildings('weather_zone', period)
        heating_hours = parameters(period).HEAB.F4.cooling_and_heating_hours.heating_hours[weather_zone]
        heating_annual_energy_use = heating_power_input * heating_hours
        return heating_annual_energy_use


class DR_AC_heating_power_input(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the heating power input for Activity Definition F4?'


class DR_AC_ProductClass(Enum):
    product_class_one = 'Product is in Product Class 1.'
    product_class_two = 'Product is in Product Class 2.'
    product_class_three = 'Product is in Product Class 3.'
    product_class_four = 'Product is in Product Class 4.'
    product_class_five = 'Product is in Product Class 5.'
    product_class_six = 'Product is in Product Class 6.'
    product_class_seven = 'Product is in Product Class 7.'
    product_class_eight = 'Product is in Product Class 8.'
    product_class_nine = 'Product is in Product Class 9.'
    product_class_ten = 'Product is in Product Class 10.'
    product_class_eleven = 'Product is in Product Class 11.'
    product_class_twelve = 'Product is in Product Class 12.'
    product_class_thirteen = 'Product is in Product Class 13.'
    product_class_fourteen = 'Product is in Product Class 14.'
    product_class_fifteen = 'Product is in Product Class 15.'
    product_class_sixteen = 'Product is in Product Class 16.'
    product_class_seveteen = 'Product is in Product Class 17.'
    product_class_eighteen = 'Product is in Product Class 18.'
    product_class_nineteen = 'Product is in Product Class 19.'
    product_class_twenty = 'Product is in Product Class 20.'
    product_class_twenty_one = 'Product is in Product Class 21.'


class DR_AC_product_class(Variable):
    value_type = Enum
    possible_values = DR_AC_ProductClass
    default_value = DR_AC_ProductClass.product_class_one
    entity = Building
    definition_period = ETERNITY
    label = 'What is the product class for the new End User Equipment?'
