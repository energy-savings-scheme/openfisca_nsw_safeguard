# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEAB_install_new_liquid_chilling_package_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition ESS_HEAB_install_new_liquid_chilling_package?'

    def formula(buildings, period, parameters):
        IPLV = buildings('ESS_HEAB_install_new_liquid_chilling_package_integrated_part_load_value', period)
        cooling_capacity = buildings('ESS_HEAB_install_new_liquid_chilling_package_cooling_capacity', period)
        LCP_type = buildings('ESS_HEAB_install_new_liquid_chilling_package_LCP_type', period)
        capacity = select([cooling_capacity >= 350 and cooling_capacity <= 499,
                           cooling_capacity >= 500 and cooling_capacity <= 699,
                           cooling_capacity >= 700 and cooling_capacity <= 999,
                           cooling_capacity >= 1000 and cooling_capacity <= 1499,
                           cooling_capacity > 1500],
                          ['350_to_499_kWR',
                           '500_to_699_kWR',
                           '700_to_999_kWR',
                           '1000_to_1499_kWR',
                           'greater_than_1500_kWR'])
        baseline = parameters(period).ESS.HEAB.table_ESS_HEAB_install_new_liquid_chilling_package_1.IPLV[LCP_type][capacity]
        baseline = parameters(period).ESS.HEAB.table_ESS_HEAB_install_new_liquid_chilling_package_1.equivalent_full_load_hours[LCP_type][capacity]
        lifetime = parameters(period).HEAB.ESS_HEAB_install_new_liquid_chilling_package.lifetime
        MWh_conversion = parameters(period).general_ESS.unit_conversion_factors['kWh_to_MWh']
        energy_savings = ((((cooling_capacity / baseline) - (cooling_capacity / IPLV))
                         * EFLH * lifetime) / MWh_conversion)
        return energy_savings


class LCPType(Enum):
    air_cooled = 'Product is an air-cooled LCP.'
    water_cooled = 'Product is a water-cooled LCP.'


class ESS_HEAB_install_new_liquid_chilling_package_LCP_type(Variable):
    value_type = Enum
    possible_values = LCPType
    default_value = LCPType.air_cooled
    entity = Building
    definition_period = ETERNITY
    label = 'What is the product type for the new liquid chilled package End' \
            ' User Equipment?'


class ESS_HEAB_install_new_liquid_chilling_package_integrated_part_load_value(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the integrated part load value for the new Liquid' \
            ' Chilling Package, as determined using AS 4776?'


class ESS_HEAB_install_new_liquid_chilling_package_cooling_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the total rated cooling capacity for the new Liquid' \
            ' Chilling Package, in kWR, as determined using AS 4776?'
