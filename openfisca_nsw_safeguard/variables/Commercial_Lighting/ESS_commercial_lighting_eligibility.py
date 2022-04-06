from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY, YEAR
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

import numpy as np
from datetime import date

from openfisca_nsw_safeguard.variables.ESS_lighting_common_variables import LightingEquipmentClass

class ESS_CL_is_eligible_for_commercial_lighting(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible for the Commercial Lighting method,' \
            ' as detailed in Clause 9.4?'

    def formula(buildings, period, parameters):
        is_eligible_activity_type = buildings('ESS_CL_is_eligible_activity_type', period)
        meets_building_upgrade_requirements = (buildings(
            'ESS_CL_building_lighting_upgrade_meets_requirements', period)) # note logic contained in this variable - 
                                                                            # traffic and public spaces will always meet this eligibility criteria
                                                                            # as it does not apply to them 
        meets_traffic_signals_upgrade_requirements = (buildings(
            'ESS_CL_traffic_signals_lighting_upgrade_meets_requirements', period)) # same as above, but for traffic signals
        meets_roads_and_public_spaces_upgrade_requirements = (buildings(
            'ESS_CL_road_and_public_spaces_lighting_upgrade_meets_requirements', period)) # same as above, but for roads and public spaces
        has_minimum_copayment_requirement = buildings('ESS_CL_minimum_copayment_amount_has_been_paid', period)
        is_eligible_equipment_type = buildings('ESS_CL_is_eligible_end_user_equipment_type', period)
        return (
            is_eligible_activity_type *
            meets_building_upgrade_requirements *
            meets_traffic_signals_upgrade_requirements * 
            meets_roads_and_public_spaces_upgrade_requirements *
            has_minimum_copayment_requirement * 
            is_eligible_equipment_type
        )

class ESS_CL_is_eligible_activity_type(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Commercial Lighting an eligible activity type?'

    def formula(buildings, period, parameters):
        is_lighting_for_roads_and_public_spaces = (
            buildings('ESS_CL_is_lighting_for_roads_and_public_spaces', period))
        is_lighting_for_traffic_signals = (
            buildings('ESS_CL_is_traffic_signals', period))
        is_building_lighting = (
            buildings('ESS_CL_is_building_lighting', period))


class ESS_CL_is_lighting_for_roads_and_public_spaces(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a lighting upgrade for Roads and Public Spaces?'


class ESS_CL_is_traffic_signals(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a lighting upgrade for Traffic Lighting?'


class ESS_CL_is_building_lighting(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a lighting upgrade for Building Lighting?'


class ESS_CL_meets_or_exceeds_relevant_lighting_standards(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the upgrade meet or exceed the relevant standards for' \
            ' each upgrade, as determined by the Scheme Administrator?'


class ESS_CL_building_lighting_upgrade_meets_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the upgrade is a Building Lighting upgrade, does it meet the' \
            ' additional requirements relevant to Building Lighting upgrades?'

    def formula(buildings, period, parameters):
        is_building_lighting_upgrade = buildings('ESS_CL_is_building_lighting', period)
        meets_AS1680_requirements = buildings('ESS_CL_building_upgrade_meets_relevant_AS1680_requirements', period)
        meets_BCA_requirements = buildings('ESS_CL_building_upgrade_meets_relevant_BCA_requirements', period)
        under_maximum_IPD = buildings('ESS_CL_building_upgrade_has_IPD_under_maximum_allowable_IPD', period)
        meets_other_administrative_requirements = buildings('ESS_CL_building_upgrade_meets_other_adminstrative_requirements', period)
        return (
                    (is_building_lighting_upgrade *
                    meets_AS1680_requirements *
                    meets_BCA_requirements *
                    under_maximum_IPD *
                    meets_other_administrative_requirements
                    )
                    +
                np.logical_not(is_building_lighting_upgrade)
        )


class ESS_CL_building_upgrade_meets_relevant_AS1680_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the lighting upgrade is a building upgrade, does it meet the relevant requirements in AS 1680?'


class ESS_CL_building_upgrade_meets_relevant_BCA_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the lighting upgrade is a building upgrade, does it meet the relevant requirements in BCA section F4.4?'


class ESS_CL_building_upgrade_has_IPD_under_maximum_allowable_IPD(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the lighting upgrade is a building upgrade, does it have an IPD less than' \
            ' or equal to the maximum IPD for each space, as defined in the Part J6 of the BCA?'


class ESS_CL_building_upgrade_meets_other_adminstrative_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the lighting upgrade is a building upgrade, does it meet other requirements as defined by the Scheme Administrator?'


class ESS_CL_minimum_copayment_amount_has_been_paid(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the minimum copayment amount of $5 per MWh of energy saved been paid?'

    def formula(buildings, period, parameters):
        copayment_amount = buildings('ESS_CL_copayment_amount', period)
        electricity_savings = buildings("ESS_CL_electricity_savings", period)
        minimum_copayment_amount = 5
        return (
                (
                    copayment_amount / electricity_savings) >
                    minimum_copayment_amount
        )


class ESS_CL_lighting_new_lamp_type(Variable):
    value_type = Enum
    possible_values = LightingEquipmentClass
    default_value = LightingEquipmentClass.T12_linear
    entity = Building
    definition_period = ETERNITY
    label = 'Defines the new lamp type, as defined in Table A9.1 or Table A9.3' \
            ' in Schedule A.'


class ESS_CL_is_eligible_end_user_equipment_type(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the item of End-User Equipment eligible?'

    def formula(buildings, period, parameters):
        new_lamp_type = buildings('ESS_CL_lighting_new_lamp_type', period)
        LightingEquipmentClass = new_lamp_type.possible_values
        is_not_eligible = (new_lamp_type == LightingEquipmentClass.is_not_eligible)
        return np.logical_not(is_not_eligible)

class ESS_CL_road_and_public_spaces_lighting_upgrade_meets_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the relevant Road and Public Spaces Lighting Upgrade meet specific requirements?'

    def formula(buildings, period, parameters):
        is_road_and_public_spaces_upgrade = buildings('ESS_CL_is_lighting_for_roads_and_public_spaces', period)
        meets_AS1158_requirements = (
            buildings('ESS_CL_roads_and_public_spaces_upgrade_meets_AS_1158_requirements', period))
        meets_administrator_requirements = (
            buildings('ESS_CL_roads_and_public_spaces_upgrade_meets_scheme_administrator_requirements', period))
        return(
            (
                is_road_and_public_spaces_upgrade *
                meets_AS1158_requirements *
                meets_administrator_requirements) +
            np.logical_not(is_road_and_public_spaces_upgrade)        
        )        


class ESS_CL_roads_and_public_spaces_upgrade_meets_AS_1158_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Roads and Public Spaces Upgrade' \
            ' meet the relevant requirements of AS 1158?'


class ESS_CL_roads_and_public_spaces_upgrade_meets_scheme_administrator_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Roads and Public Spaces Upgrade meet' \
            ' other standards or benchmarks, specified by the Scheme Administrator?'


class ESS_CL_traffic_signals_lighting_upgrade_meets_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the relevant Traffic Signals lighting upgrade meet specific requirements?'

    def formula(buildings, period, parameters):
        is_traffic_signals_upgrade = buildings('ESS_CL_is_traffic_signals', period)
        meets_AS2144_requirements = (
            buildings('ESS_CL_traffic_signals_upgrade_meets_scheme_administrator_requirements', period))
        meets_administrator_requirements = (
            buildings('ESS_CL_roads_and_public_spaces_upgrade_meets_scheme_administrator_requirements', period))
        return(
            (
                is_traffic_signals_upgrade *
                meets_AS2144_requirements *
                meets_administrator_requirements) +
            np.logical_not(is_traffic_signals_upgrade)        
        )        


class ESS_CL_traffic_signals_upgrade_meets_AS_2144_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Traffic Signals Upgrade' \
            ' meet the relevant requirements of AS 2144?'


class ESS_CL_traffic_signals_upgrade_meets_scheme_administrator_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Traffic Signals upgrade meet' \
            ' other standards or benchmarks, specified by the Scheme Administrator?'


class ESS_CL_(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the lighting upgrade is a building upgrade, does it have an IPD less than' \
            ' or equal to the maximum IPD for each space, as defined in the Part J6 of the BCA?'
