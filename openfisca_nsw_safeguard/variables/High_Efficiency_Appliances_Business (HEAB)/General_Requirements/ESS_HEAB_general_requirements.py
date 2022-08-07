from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np



class ESS_HEAB_activity_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet the Equipment Requirements defined' \
            ' in the relevant Activity Definition in Schedule F?'

    def formula(buildings, period, parameters):
        activity_definition = buildings('ESS_activity_definition', period)
        ActivityDefinition = (activity_definition.possible_values)
        relevant_equipment_requirements = np.select(
                                                        [
                                                            activity_definition == ActivityDefinition.F1_1,
                                                            activity_definition == ActivityDefinition.F1_2,
                                                            np.logical_not(
                                                                    (
                                                                        activity_definition == ActivityDefinition.F1_1
                                                                    ) +
                                                                    (
                                                                        activity_definition == ActivityDefinition.F1_2
                                                                    )
                                                                    )
                                                        ],
            [
                buildings(
                    'ESS_HEAB_install_refrigerated_cabinet_meets_equipment_requirements', period),
                buildings(
                    'ESS_HEAB_replace_refrigerated_cabinet_meets_equipment_requirements', period),
                True
            ]
            )

        return(
            relevant_equipment_requirements
            )


class ESS_HEAB_activity_meets_installation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet the Equipment Requirements defined' \
            ' in the relevant Activity Definition in Schedule F?'

    def formula(buildings, period, parameters):
        activity_definition = buildings('ESS_activity_definition', period)
        ActivityDefinition = (activity_definition.possible_values)
        relevant_installation_requirements = np.select(
                                                        [
                                                            activity_definition == ActivityDefinition.F1_1,
                                                            activity_definition == ActivityDefinition.F1_2,
                                                            np.logical_not(
                                                                    (
                                                                        activity_definition == ActivityDefinition.F1_1
                                                                    ) +
                                                                    (
                                                                        activity_definition == ActivityDefinition.F1_2
                                                                    )
                                                                    )
                                                        ],
            [
                buildings(
                    'ESS_HEAB_install_refrigerated_cabinet_meets_installation_requirements', period),
                buildings(
                    'ESS_HEAB_replace_refrigerated_cabinet_meets_installation_requirements', period),
                True
            ]
            )

        return(
            relevant_installation_requirements
            )


class ESS_HEAB_activity_paid_copayment_amount(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the copayment amount that has been made?'


class ESS_HEAB_activity_required_copayment_amount_is_paid(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If a copayment is required, has the copayment been paid?'

    def formula(buildings, period, parameters):
        activity_definition = buildings('ESS_activity_definition', period)
        ActivityDefinition = (activity_definition.possible_values)
        copayment_is_required = (
                                    (activity_definition == ActivityDefinition.F1_1) +
                                    (activity_definition == ActivityDefinition.F1_2)
                                )

        number_of_RCs_installed = buildings(
            'ESS_HEAB_number_of_RCs_installed', period)
        copayment_amount_per_RC = 250
        total_copayment_amount = (
            number_of_RCs_installed *
            copayment_amount_per_RC
        )

        paid_copayment_amount = buildings(
            'ESS_HEAB_activity_paid_copayment_amount', period)
        
        return (
            (paid_copayment_amount >= total_copayment_amount) +
            np.logical_not(copayment_is_required)
        )


class ESS_HEAB_meets_all_general_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the general HEAB requirements defined in clause 9.9?'

    def formula(buildings, period, parameters):
        activity_definition = buildings('ESS_activity_definition', period)
        ActivityDefinition = (activity_definition.possible_values)
        
        BCA_building_class = buildings('BCA_building_class', period)
        BuildingClass = BCA_building_class.possible_values

        is_residential = (
                            (BCA_building_class == BuildingClass.BCA_Class_1a) +
                            (BCA_building_class == BuildingClass.BCA_Class_1b) +
                            (BCA_building_class == BuildingClass.BCA_Class_2) +
                            (BCA_building_class == BuildingClass.BCA_Class_4)
        )

        is_eligible_residential_activity = (
                                                (activity_definition == ActivityDefinition.F4) *
                                                (BCA_building_class == BuildingClass.BCA_Class_2)
                                            )

        meets_equipment_requirements = buildings(
            'ESS_HEAB_activity_meets_equipment_requirements', period) 
        meets_installation_requirements = buildings(
            'ESS_HEAB_activity_meets_installation_requirements', period)
        is_not_eligible_residential_activity = (
            np.logical_not(is_residential) +
            is_eligible_residential_activity)
        copayment_is_made = buildings(
            'ESS_HEAB_activity_required_copayment_amount_is_paid', period)

        return (
            meets_equipment_requirements *
            meets_installation_requirements *
            is_not_eligible_residential_activity *
            copayment_is_made
        )