from email.mime import base
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY, YEAR
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

import numpy as np
from datetime import date


class ESS_CL_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the Electricity Savings created from the' \
            ' commercial lighting implementation?'

    def formula(buildings, period, parameters):
        baseline_consumption = buildings('ESS_CL_baseline_consumption', period)
        upgrade_consumption = buildings('ESS_CL_upgrade_consumption')
        regional_network_factor = buildings('ESS__regional_network_factor', period)
        return(
            (
                baseline_consumption - 
                upgrade_consumption
                ) *
            regional_network_factor
        )


class ESS_CL_baseline_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the baseline consumption for use in calculating Electricity Savings' \
            ' for the Commercial Lighting method?'

    def formula(buildings, period, parameters):
        # import relevant variables
        default_LCP = buildings('ESS_CL_default_LCP', period)
        asset_lifetime = buildings('ESS_CL_asset_lifetime', period)
        annual_operating_hours = buildings('ESS_CL_default_annual_operating_hours', period)
        control_multiplier = buildings('ESS_CL_control_multiplier', period)
        air_conditioning_multiplier = buildings('ESS_CL_air_conditioning_multiplier', period)
        maximum_allowable_IPD = buildings('ESS_CL_maximum_allowable_IPD', period)
        area = buildings('ESS_CL_area', period)

        # below is equation 7 baseline consumption

        equation_7_baseline_consumption = (
            default_LCP *
            asset_lifetime *
            annual_operating_hours *
            control_multiplier *
            air_conditioning_multiplier /
            1000000
        )

        # below is equation 8 baseline consumption

        equation_8_baseline_consumption = (
            maximum_allowable_IPD * 
            area * 
            asset_lifetime *
            annual_operating_hours *
            air_conditioning_multiplier /
            1000000
        )

        # logic to choose whether to use equation 7 or equation 8

        upgrade_required_to_comply_with_BCA_J6 = (
            buildings('ESS_CL_upgrade_is_required_to_comply_with_BCA_J6', period))
        existing_lighting_meets_IPD_requirements = (buildings('ESS_CL_existing_lighting_meets_IPD_requirements'), period)
        baseline_consumption = np.where(
                                        (   
                                            upgrade_required_to_comply_with_BCA_J6 *
                                            np.logical_not(existing_lighting_meets_IPD_requirements)
                                        ),
                                        equation_8_baseline_consumption,
                                        equation_7_baseline_consumption
                                        )

        return baseline_consumption