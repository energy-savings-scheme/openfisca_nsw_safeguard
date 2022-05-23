from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

class ESS_ROOA_remove_spare_refrigerator_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the Eligibility' \
            ' Requirements defined in Removal of Old Appliance (fridge)?'
    metadata = {
        'alias': "ROOA meets eligibility requirements",
    }

    def formula(buildings, period, parameters):
        is_residential = buildings(
            'Appliance_located_in_residential_building', period)
        is_fridge = buildings('Fridge_is_classified_as_refrigerator', period)
        is_more_than_200L = buildings('Fridge_capacity_more_than_200L', period)
        is_working = buildings(
            'Fridge_in_working_order', period)
        another_primary_fridge = buildings(
            'another_fridge_provides_primary_refrigeration', period)
        one_fewer_fridge_after_activity = buildings(
            'Fridge_total_number_one_less', period)

        return (
                is_residential *
                is_fridge *
                is_more_than_200L *
                is_working *
                another_primary_fridge *
                one_fewer_fridge_after_activity
                )


class ESS_ROOA_remove_spare_refrigerator_meets_all_requirements(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    label = 'Does the implementation meet all of the' \
            ' Requirements defined in Removal of Old Appliance (fridge)?'
    metadata = {
        'alias': "ROOA meets all requirements",
    }

    def formula(buildings, period, parameters):
        meets_equipment_requirements = buildings('ESS_ROOA_remove_spare_refrigerator_meets_equipment_requirements', period)
        return meets_equipment_requirements
