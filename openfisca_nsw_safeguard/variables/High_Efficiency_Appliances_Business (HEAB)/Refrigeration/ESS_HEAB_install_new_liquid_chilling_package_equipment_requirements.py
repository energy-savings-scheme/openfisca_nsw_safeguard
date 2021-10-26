from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np



class ESS_HEAB_install_new_liquid_chilling_package_is_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product registered in GEMS?'
    # a way you could operationalise this - link in w. GEMS Registry and see if \
    # the product is registered based on user input. You could also pull a \
    # dropdown from said Registry in the form of an Enum?


class ESS_HEAB_install_new_liquid_chilling_package_complies_with_GEMS_2012_LCP(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product comply with the Greenhouse and Energy Minimum' \
            ' Standards (Liquid-chilling Packages Using the Vapour' \
            ' Compression Cycle) Determination 2012?'
    # what does complying with this Determination mean?


class ESS_HEAB_install_new_liquid_chilling_package_IPLV_10_percent_higher_than_baseline(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product have an IPLV at least 10% higher than the' \
            ' baseline for the corresponding type and cooling capacity,' \
            ' detailed in Table ESS_HEAB_install_new_liquid_chilling_package.1?'
    # what does complying with this Determination mean?

    def formula(buildings, period, parameters):
        IPLV = buildings('ESS_HEAB_install_new_liquid_chilling_package_integrated_part_load_value', period)
        cooling_capacity = buildings('ESS_HEAB_install_new_liquid_chilling_package_cooling_capacity', period)
        LCP_type = buildings('ESS_HEAB_install_new_liquid_chilling_package_LCP_type', period)
        capacity = select([
                                
                            cooling_capacity >= 350 and cooling_capacity <= 499,
                            cooling_capacity >= 500 and cooling_capacity <= 699,
                            cooling_capacity >= 700 and cooling_capacity <= 999,
                            cooling_capacity >= 1000 and cooling_capacity <= 1499,
                            cooling_capacity > 1500],
                          [
                            '350_to_499_kWR',
                            '500_to_699_kWR',
                            '700_to_999_kWR',
                            '1000_to_1499_kWR',
                            'greater_than_1500_kWR'])
        baseline = parameters(period).ESS.HEAB.table_F2_1[LCP_type][capacity]
        percentage_increase = ((IPLV - baseline) * 100)  # i'm sure there's a more efficient way to write this
        return percentage_increase > 10


class ESS_HEAB_install_new_liquid_chilling_package_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F4?'

    def formula(buildings, period, parameters):
        registered_in_GEMS = buildings('ESS_HEAB_install_new_liquid_chilling_package_is_registered_in_GEMS', period)
        complies_with_GEMS_2012 = buildings('ESS_HEAB_install_new_liquid_chilling_package_complies_with_GEMS_2012_LCP', period)
        IPLV_higher_than_baseline = buildings('ESS_HEAB_install_new_liquid_chilling_package_IPLV_10_percent_higher_than_baseline', period)
        return (registered_in_GEMS * complies_with_GEMS_2012 * IPLV_higher_than_baseline)
