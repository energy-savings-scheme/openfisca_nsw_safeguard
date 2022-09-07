from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np


class ESS_MethodType(Enum):
    clause_7_PIAM = 'Certificates are created under clause 7, within the PIAM method.'
    clause_7A_PIAMV = 'Certificates are created under clause 7A, within the PIAM&V method.'
    clause_8_5_MBM_baseline_per_output = 'Certificates are created under clause 8.5, within the MBM (Baseline per unit of output) method.'
    clause_8_6_MBM_unaffected_output = 'Certificates are created under clause 8.6, within the MBM (Baseline unaffected by output) method.'
    clause_8_7_MBM_normalised_baseline = 'Certificates are created under clause 8.7, within the MBM (Normalised baseline) method.'
    clause_8_8_NABERS = 'Certificates are created under clause 8.8, within the NABERS method.'
    clause_8_9_AMB = 'Certificates are created under clause 8.9, within the AMB method.'
    clause_9_3_SONA = 'Certificates are created under clause 9.3, within the SONA method.'
    clause_9_4_CL = 'Certificates are created under clause 9.4, within the Commercial Lighting method.'
    clause_9_4A_PL = 'Certificates are created under clause 9.4A, within the Public Lighting method.'
    clause_9_5_HEM = 'Certificates are created under clause 9.5, within the High Efficiency Motors method.'
    clause_9_6_PFC = 'Certificates are created under clause 9.6, within the Power Factor Correction method.'
    clause_9_7_ROOA = 'Certificates are created under clause 9.7, within the Removal of Old Appliances method.'
    clause_9_8_HEER = 'Certificates are created under clause 9.8, within the HEER method.'
    clause_9_9_HEAB = 'Certificates are created under clause 9.9, within the HEAB method.'
    # there is probably a fancier and easier way to do this which interfaces with regulation_reference.py \
    # but this works for now



class ESS__method_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = ESS_MethodType
    default_value = ESS_MethodType.clause_8_8_NABERS
    definition_period = ETERNITY
    label = 'What method of the ESS are the Energy Savings Certificates being' \
            ' created within?'
    metadata={
        "variable-type": "user-input",
        "alias":"ESS Method Type",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Energy Savings Scheme - General'
        }
    # used to determine what general requirements to pull into eligibility criteria calculations


    def formula(buildings, period, parameters):
        activity_definition = buildings('ESS_activity_definition', period)

        # reminder that you can manually set a value for the above in whatever app you're building and do not
        # need the activity definition to set a method type value, if you build your app to select it.
        # this is especially relevant for metered activities. I'm defaulting the value to NABERS \ 
        # to ensure the ESC Calculator still functions

        is_SONA_activity = (
                                (
                                    activity_definition == ESS_ActivityDefinition.B1
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.B2
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.B3
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.B4
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.B5
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.B6
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.B7
                                )
                            )

        is_ROOA_activity = (
                                (
                                    activity_definition == ESS_ActivityDefinition.C1
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.C2
                                )
                            )

        is_HEER_schedule_D_activity = (
                                (
                                    activity_definition == ESS_ActivityDefinition.D1
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D2
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D3
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D4
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D5
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D6
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D7
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D8
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D9
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D10
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D11
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D12
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D13
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D14
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D15
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D16
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D17
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D18
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D19
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D20
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.D21
                                ) 
                            )

        is_HEER_schedule_E_activity = (
                                (
                                    activity_definition == ESS_ActivityDefinition.E1
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E2
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E3
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E4
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E5
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E6
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E7
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E8
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E9
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E10
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E11
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E12
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.E13
                                )
                            )

        is_HEAB_activity = (
                                (
                                    activity_definition == ESS_ActivityDefinition.F1_1
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F1_2
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F2
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F3
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F4
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F5
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F6
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F7
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F8
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F9
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F10
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F11
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F12
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F13
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F14
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F15
                                ) +
                                (
                                    activity_definition == ESS_ActivityDefinition.F16
                                )     
                            )

        method_type = np.select(
                            [
                                is_SONA_activity,
                                is_ROOA_activity,
                                is_HEER_schedule_D_activity,
                                is_HEER_schedule_E_activity,
                                is_HEAB_activity,
                                np.logical_not(
                                                    (
                                                        is_SONA_activity +
                                                        is_ROOA_activity +
                                                        is_HEER_schedule_D_activity +
                                                        is_HEER_schedule_E_activity +
                                                        is_HEAB_activity
                                                    )
                                                )
                            ],
                            [
                                (ESS_MethodType.clause_9_3_SONA),
                                (ESS_MethodType.clause_9_7_ROOA),
                                (ESS_MethodType.clause_9_8_HEER),
                                (ESS_MethodType.clause_9_8_HEER),
                                (ESS_MethodType.clause_9_9_HEAB),
                                (ESS_MethodType.clause_8_8_NABERS)
                            ]
                        )     

        return method_type


class ESS_ActivityDefinition(Enum):
    B1 = 'Certificates are created under Activity Definition B1.'
    B2 = 'Certificates are created under Activity Definition B2.'
    B3 = 'Certificates are created under Activity Definition B3.'
    B4 = 'Certificates are created under Activity Definition B4.'
    B5 = 'Certificates are created under Activity Definition B5.'
    B6 = 'Certificates are created under Activity Definition B6.'
    B7 = 'Certificates are created under Activity Definition B7.'
    C1 = 'Certificates are created under Activity Definition C1.'
    C2 = 'Certificates are created under Activity Definition C2.'
    D1 = 'Certificates are created under Activity Definition D1.'
    D2 = 'Certificates are created under Activity Definition D2.'
    D3 = 'Certificates are created under Activity Definition D3.'
    D4 = 'Certificates are created under Activity Definition D4.'
    D5 = 'Certificates are created under Activity Definition D5.'
    D6 = 'Certificates are created under Activity Definition D6.'
    D7 = 'Certificates are created under Activity Definition D7.'
    D8 = 'Certificates are created under Activity Definition D8.'
    D9 = 'Certificates are created under Activity Definition D9.'
    D10 = 'Certificates are created under Activity Definition D10.'
    D11 = 'Certificates are created under Activity Definition D11.'
    D12 = 'Certificates are created under Activity Definition D12.'
    D13 = 'Certificates are created under Activity Definition D13.'
    D14 = 'Certificates are created under Activity Definition D14.'
    D15 = 'Certificates are created under Activity Definition D15.'
    D16 = 'Certificates are created under Activity Definition D16.'
    D17 = 'Certificates are created under Activity Definition D17.'
    D18 = 'Certificates are created under Activity Definition D18.'
    D19 = 'Certificates are created under Activity Definition D19.'
    D20 = 'Certificates are created under Activity Definition D20.'
    D21 = 'Certificates are created under Activity Definition D21.'
    E1 = 'Certificates are created under Activity Definition E1.'
    E2 = 'Certificates are created under Activity Definition E2.'
    E3 = 'Certificates are created under Activity Definition E3.'
    E4 = 'Certificates are created under Activity Definition E4.'
    E5 = 'Certificates are created under Activity Definition E5.'
    E6 = 'Certificates are created under Activity Definition E6.'
    E7 = 'Certificates are created under Activity Definition E7.'
    E8 = 'Certificates are created under Activity Definition E8.'
    E9 = 'Certificates are created under Activity Definition E9.'
    E10 = 'Certificates are created under Activity Definition E10.'
    E11 = 'Certificates are created under Activity Definition E11.'
    E12 = 'Certificates are created under Activity Definition E12.'
    E13 = 'Certificates are created under Activity Definition E13.'
    F1_1 = 'Certificates are created under Activity Definition F1.1.'
    F1_2 = 'Certificates are created under Activity Definition F1.2.'
    F2 = 'Certificates are created under Activity Definition F2.'
    F3 = 'Certificates are created under Activity Definition F3.'
    F4 = 'Certificates are created under Activity Definition F4.'
    F5 = 'Certificates are created under Activity Definition F5.'
    F6 = 'Certificates are created under Activity Definition F6.'
    F7 = 'Certificates are created under Activity Definition F7.'
    F8 = 'Certificates are created under Activity Definition F8.'
    F9 = 'Certificates are created under Activity Definition F9.'
    F10 = 'Certificates are created under Activity Definition F10.'
    F11 = 'Certificates are created under Activity Definition F11.'
    F12 = 'Certificates are created under Activity Definition F12.'
    F13 = 'Certificates are created under Activity Definition F13.'
    F14 = 'Certificates are created under Activity Definition F14.'
    F15 = 'Certificates are created under Activity Definition F15.'
    F16 = 'Certificates are created under Activity Definition F16.'
    not_defined_activity = 'Certificates are created under a method that is not defined in Schedules B through F.'


class ESS_activity_definition(Variable):
    value_type = Enum
    entity = Building
    possible_values = ESS_ActivityDefinition
    default_value = ESS_ActivityDefinition.not_defined_activity
    definition_period = ETERNITY
    label = 'What activity definition is being used for the Implementation?'
    metadata={
        "variable-type": "user-input",
        "alias":"ESS Method Type",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Energy Savings Scheme - General'
        }
