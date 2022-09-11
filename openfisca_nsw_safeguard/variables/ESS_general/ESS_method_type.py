from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS_MethodType(Enum):
    clause_8_6_unaffected_baseline = 'Certificates are created under clause 8.6, within the baseline unaffected by output method.'
    clause_8_7_normalised_baseline = 'Certificates are created under clause 8.7, within the normalised baseline method.'
    clause_8_8_NABERS = 'Certificates are created under clause 8.8, within the NABERS method.'
    clause_8_9_AMB = 'Certificates are created under clause 8.9, within the AMB method.'
    clause_9_3_SONA = 'Certificates are created under clause 9.3, within the SONA method.'
    clause_9_4_CL = 'Certificates are created under clause 9.4, within the CL method.'
    clause_9_4A_PL = 'Certificates are created under clause 9.4A, within the PL method.'
    clause_9_5_HEM = 'Certificates are created under clause 9.5, within the HEM method.'
    clause_9_6_PFC = 'Certificates are created under clause 9.6, within the PFC method.'
    clause_9_7_ROOA = 'Certificates are created under clause 9.7, within the ROOA method.'
    clause_9_8_HEER = 'Certificates are created under clause 9.8, within the HEER method.'
    clause_9_9_HEAB = 'Certificates are created under clause 9.9, within the HEAB method.'


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
    no_activity_definition = 'Certificates are not created under an Activity Definition defined' \
        ' in Schedules B through F.'


class ESS_activity_definition(Variable):
    value_type = Enum
    entity = Building
    possible_values = ESS_ActivityDefinition
    default_value = ESS_ActivityDefinition.F1_1
    definition_period = ETERNITY
    label = 'What activity definition is being used for the Implementation?'
    metadata={
        "variable-type": "user-input",
        "alias":"ESS Method Type",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Energy Savings Scheme - General'
        }
