from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class RefrigeratorGroup(Enum):
    group_1 = u"Refrigerator is in Group 1."
    group_2 = u"Refrigerator is in Group 2."
    group_3 = u"Refrigerator is in Group 3."
    group_4 = u"Refrigerator is in Group 4."
    group_5B = u"Refrigerator is in Group 5B."
    group_5S = u"Refrigerator is in Group 5S."
    group_5T = u"Refrigerator is in Group 5T."
    group_6C = u"Refrigerator is in Group 6C."
    group_6U = u"Refrigerator is in Group 6U."
    group_7 = u"Refrigerator is in Group 7."
    #  need to put in what activities this is relevant for
\
class refrigerator_or_freezer_group(Variable):
    value_type = Enum
    entity = Building
    possible_values = RefrigeratorGroup
    default_value = RefrigeratorGroup.group_1
    definition_period = ETERNITY
    label = "What is the refrigerator group for the new End User Equipment?"
    #  need to put in what activities this is relevant for

class refrigerator_or_freezer_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the capacity of the refrigerator or freezer, in L?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1, Equipment Requirement 3.'
    #  need to put in what activities this is relevant for


class number_of_refrigerator_doors(Variable):
    value_type = int  # note need to recode as Enum once reading AS2040
    entity = Building
    definition_period = ETERNITY
    label = 'How many doors does the refrigerator have?'
    # for use in Activity Definition B4, B5.
