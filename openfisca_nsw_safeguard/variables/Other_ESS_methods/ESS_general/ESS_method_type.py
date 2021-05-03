from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS_MethodType(Enum):
    clause_8_8_NABERS = 'Certificates are created under clause 8.8, within the NABERS method.'
    clause_9_8_HEER = 'Certificates are created under clause 9.8, within the HEER method.'


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
