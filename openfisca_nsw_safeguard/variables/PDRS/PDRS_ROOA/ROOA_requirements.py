from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022

class PDRS_ROOA_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Implementation' \
            ' Requirements defined in Removal of Old Appliance (fridge)?'
    metadata = {
        'alias': "ROOA meets implementation requirements",
        "regulation_reference": PDRS_2022["8","5"]
    }

    def formula(buildings, period, parameters):
        one_less = buildings('Fridge_total_number_one_less', period)
        not_primary = buildings('Fridge_not_primary', period)
        is_removed = buildings('Appliance_is_removed', period)
        follows_removal_requirements = buildings(
            'Appliance_follows_removal_requirements', period)
        return not_primary * is_removed * follows_removal_requirements * one_less


class PDRS_ROOA_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Eligibility' \
            ' Requirements defined in Removal of Old Appliance (fridge)?'
    metadata = {
        'alias': "ROOA meets eligibility requirements",
        "regulation_reference": PDRS_2022["8","5"]
    }

    def formula(buildings, period, parameters):
        is_residential = buildings(
            'Appliance_located_in_residential_building', period)

        is_small_biz = buildings(
            'Appliance_located_in_small_biz_building', period)
        return is_residential + is_small_biz


class PDRS_ROOA_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Equipment' \
            ' Requirements defined in Removal of Old Appliance (fridge)?'
    metadata = {
        'alias': "ROOA meets equipment requirements",
        "regulation_reference": PDRS_2022["8","5"]
    }

    def formula(buildings, period, parameters):
        is_working = buildings(
            'Fridge_in_working_order', period)
        is_more_than_200L = buildings('Fridge_capacity_more_than_200L', period)
        is_fridge = buildings('Fridge_is_classified_as_refrigerator', period)
        return is_working * is_more_than_200L * is_fridge


class PDRS_ROOA_meets_all_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the' \
            ' Requirements defined in Removal of Old Appliance (fridge)?'
    metadata = {
        'alias': "ROOA meets all requirements",
        "regulation_reference": PDRS_2022["8","5"]
    }

    def formula(buildings, period, parameters):
        implementation = buildings(
            'PDRS_ROOA_meets_implementation_requirements', period)
        eligibility = buildings(
            'PDRS_ROOA_meets_eligibility_requirements', period)
        equipment = buildings('PDRS_ROOA_meets_equipment_requirements', period)
        return implementation * eligibility * equipment
