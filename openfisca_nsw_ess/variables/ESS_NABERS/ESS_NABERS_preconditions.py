from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import datetime


def find_corresponding_date(start_date):
    day = start_date.day
    month = start_date.month
    year = start_date.year
    next_month = month + 1
    next_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1

    try:
        new_date = datetime(year=next_year, month=next_month, day=day)
    except ValueError:
        next_month = next_month + 1
        if next_month == 13:
            next_month = 1
            next_year = next_year + 1
        new_date = datetime(year=next_year, month=next_month, day=1)
        return new_date

    else:
        return new_date


def count_months(start_date, end_date):
    count = 0
    corres_date = start_date
    while(True):
        corres_date = find_corresponding_date(corres_date)
        # print(corres_date)
        if(corres_date > end_date):
            return count
        else:
            count = count + 1


class first_nabers_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause **"
    label="Is this the first NABERS rating for the building?"
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS First Building Rating",
        "major-cat":"Energy Savings Scheme",
        "monor-cat":'Metered Baseline Method - NABERS baseline'
        }


class rating_obtained_for_legal_requirement(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause **"
    label = 'Is the rating being obtained in order to comply with any' \
            ' mandatory legal requirement? This includes, but is not limited' \
            ' to the Commercial Building Disclosure Program.'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Obtained for Legal Requirement",
        "major-cat":"Energy Savings Scheme",
        "monor-cat":'Metered Baseline Method - NABERS baseline'
        }


class current_NABERS_star_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    reference="Clause **"
    label="What is the current NABERS star rating for the building?"
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Current Star Rating",
        "major-cat":"Energy Savings Scheme",
        "monor-cat":'Metered Baseline Method - NABERS baseline'
        }


class ESC_creation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the date on which ESCs are registered and created?'\


class ESS__NABERS_building_has_GreenPower(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.1 (b)"
    label="Does the building have any GreenPower?"
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Has Greenpower",
        "major-cat":"Energy Savings Scheme",
        "monor-cat":'Metered Baseline Method - NABERS baseline'
        }
