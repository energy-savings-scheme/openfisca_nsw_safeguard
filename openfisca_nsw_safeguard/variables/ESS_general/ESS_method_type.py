from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS_MethodType(Enum):
    clause_8_8_NABERS = 'Certificates are created under clause 8.8, within the NABERS method.'
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
