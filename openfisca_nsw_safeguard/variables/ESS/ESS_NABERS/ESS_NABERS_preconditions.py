from openfisca_core.variables import *
from openfisca_core.periods import YEAR, ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np
import datetime
import time
from datetime import datetime as py_datetime
from datetime import date

from openfisca_nsw_safeguard.regulation_reference import ESS_2021

epoch = time.gmtime(0).tm_year # epoch used to ensure current_rating year, used in A20, is calculated correctly
today_date_and_time = np.datetime64(datetime.datetime.now())
today = today_date_and_time.astype('datetime64[D]') # today is used to calculate the age of the Historical Rating

# below functions are used to calculate number of months between two input dates,
# in months, as legally defined by Section 21 of the NSW Interpretation Act (1987).
# Note that this definition differs from definitions of month defined in datetime
# or other Python libraries.

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
        new_date = py_datetime(year=next_year, month=next_month, day=day)
    except ValueError:
        next_month = next_month + 1
        if next_month == 13:
            next_month = 1
            next_year = next_year + 1
        new_date = py_datetime(year=next_year, month=next_month, day=1)
        return new_date

    else:
        return new_date


def toPyDateTime(numpyDate):
    return py_datetime.strptime(str(numpyDate), "%Y-%m-%d")


def count_months(sdate, edate):
    start_date = toPyDateTime(sdate)
    end_date = toPyDateTime(edate)
    count = 0
    corres_date = start_date
    while(True):
        corres_date = find_corresponding_date(corres_date)
        if(corres_date > end_date):
            return count
            break
        else:
            count = count + 1

# end NSW legal month calculation functions

class ESS__NABERS_rating_calculated_using_NABERS_rating_tools(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.1 (a)"
    label="Is the NABERS Rating calculated using one of the eligible NABERS" \
          " rating tools?"
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Uses Eligible Calculation Tool",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


    def formula(buildings, period, parameters):
        building_type = buildings('ESS__NABERS_building_type', period)
        BuildingType = building_type.possible_values
        return ((building_type == BuildingType.aged_care)
                + (building_type == BuildingType.apartment_building)
                + (building_type == BuildingType.data_centre)
                + (building_type == BuildingType.hospital)
                + (building_type == BuildingType.hotel)
                + (building_type == BuildingType.office)
                + (building_type == BuildingType.retirement_living)
                + (building_type == BuildingType.shopping_centre)
                )


class ESS__NABERS_building_has_GreenPower(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.1 (b)"
    label="Does the building have any GreenPower?"
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Has Greenpower",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_all_sources_of_on_site_electricity_generation_identified(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.1 (d)"
    label="Have all sources of on site electricity generation been identified?"
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS On-Site Generation Identified",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_on_site_unaccounted_electricity_metered_and_recorded(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.1 (e)"
    label="Have all sources of on site unaccounted electricity been' \
          ' metered and recorded over the Rating Period?"
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Unaccounted Electricity Metered and Recorded",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_current_NABERS_star_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    reference="Clause **"
    label='What is the current NABERS star rating for the building?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Current Star Rating",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_start_date_of_current_NABERS_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.2 (a)"
    label = 'What is the start date of the Current Rating Period as listed on' \
            ' the Current NABERS Rating Report?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Current Rating Start Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_end_date_of_current_NABERS_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.2 (a)"
    label = 'What is the end date of the Current Rating Period as listed on' \
            ' the Current NABERS Rating Report?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Current Rating End Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_current_rating_year(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the year for the current rating period?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS Current Rating Year",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        end_date_of_current_NABERS_rating_period = buildings('ESS__NABERS_end_date_of_current_NABERS_rating_period', period)
        current_rating_year = end_date_of_current_NABERS_rating_period.astype('datetime64[Y]') + epoch  # need to check if this works on Windows
        return current_rating_year


class ESS__NABERS_historical_NABERS_star_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.2 (b)"
    label='What is the current NABERS star rating for the building?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Historical Star Rating",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_start_date_of_historical_NABERS_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.2 (b)"
    label = 'What is the start date of the Current Rating Period as listed on' \
            ' the Current NABERS Rating Report?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Historical Rating Start Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_end_date_of_historical_NABERS_rating_period(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.2 (b)"
    label = 'What is the end date of the Current Rating Period as listed on' \
            ' the Current NABERS Rating Report?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Historical Rating End Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_historical_rating_year(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the year for the historical rating period?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS Historical Rating Year",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        end_date_of_historical_NABERS_rating_period = buildings('ESS__NABERS_end_date_of_historical_NABERS_rating_period', period)
        historical_rating_year = end_date_of_historical_NABERS_rating_period.astype('datetime64[Y]') + epoch  # need to check if this works on Windows
        return historical_rating_year


class ESS__NABERS_age_of_historical_rating(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.2 (b)"
    label = 'Calculate the age of the historical rating, for use in determining' \
            ' Annual Rating Adjustment from Table A21.'  # need to determine what unit is used to determine the age of the historical rating.
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS Historical Rating Age",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        hist = buildings(
            'ESS__NABERS_end_date_of_historical_NABERS_rating_period', period
            )
        age_in_days = (today.astype('datetime64[D]')
        - hist.astype('datetime64[D]')).astype('datetime64[D]')
        return age_in_days.astype('datetime64[Y]')


class ESS__NABERS_BuildingDate(Enum):
    built_before_nov_2006 = 'building was built before 1 November 2006.'
    built_after_nov_2006 = 'building was built on or after 1 November 2006.'
    # need to check if this is appropriate name for Enum.


class ESS__NABERS_building_date(Variable):
    value_type = Enum
    possible_values = ESS__NABERS_BuildingDate
    default_value = ESS__NABERS_BuildingDate.built_before_nov_2006
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.3 (a)"
    label = 'Was the building built before 1 November 2006, or on or after 1 November 2006?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Building Construction Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_exceeds_A20_benchmark_rating_by_half_star(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.3 (a) (i)"
    label='Does the current NABERS Rating exceed the Benchmark NABERS Rating from' \
          ' Table A20 by at least 0.5 stars?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS First Building Rating",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        current_NABERS_rating = buildings('ESS__NABERS_current_NABERS_star_rating', period)
        current_rating_year = np.where((buildings('ESS__NABERS_current_rating_year', period) >
                                        parameters(period).ESS.MBM.NABERS.table_a20.max_year),
                                        parameters(period).ESS.MBM.NABERS.table_a20.max_year,
                                        buildings('ESS__NABERS_current_rating_year', period))
        building_type = buildings('ESS__NABERS_building_type', period)
        building_date = buildings('ESS__NABERS_building_date', period)
        benchmark_rating = parameters(period).ESS.MBM.NABERS.table_a20.ratings_index[current_rating_year][building_type][building_date]
        return (current_NABERS_rating - benchmark_rating >= 0.5)


class ESS__NABERS_first_NABERS_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.3 (a) (ii)"
    label="Is this the first NABERS rating for the building?"
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS First Building Rating",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_rating_obtained_for_legal_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.3 (a) (iii)"
    label = 'Is the rating being obtained in order to comply with any' \
            ' mandatory legal requirement? This includes, but is not limited' \
            ' to the Commercial Building Disclosure Program.'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Obtained for Legal Requirement",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_is_eligible_for_method_one(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.3 (a)"
    label = 'Is the NABERS Rating eligible for using Calculation Method 1?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS Eligible To Use Calculation Method 1",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        is_first_NABERS_rating = buildings('ESS__NABERS_first_NABERS_rating', period)
        obtained_for_legal_requirement = buildings('ESS__NABERS_rating_obtained_for_legal_requirements', period)
        exceeds_benchmark = buildings('ESS__NABERS_exceeds_A20_benchmark_rating_by_half_star', period)
        return ((is_first_NABERS_rating)
                * (np.logical_not(obtained_for_legal_requirement))
                * (exceeds_benchmark))


class ESS__NABERS_current_star_rating_exceeds_method_two_benchmark_rating(Variable):
    value_type = bool
    entity = Building
    definition_period = YEAR
    label = 'Does the NABERS Star Rating used to calculate ESCs within' \
            ' method 1 exceed the minimum star rating?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS Current Star Rating Exceeds Method Two Benchmark Rating",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        hist_rating = buildings('ESS__NABERS_historical_NABERS_star_rating', period)
        cur_year = buildings('ESS__NABERS_current_rating_year', period)
        hist_year = buildings('ESS__NABERS_historical_rating_year', period)
        building_type = buildings("ESS__NABERS_building_type", period)
        hist_rating_age = buildings('ESS__NABERS_age_of_historical_rating', period)
        adjustment_year_string = np.where(hist_rating_age > 1,
        "two_to_seven_year_old",
        "one_year_old")
        annual_rating_adj = (parameters(period).ESS.MBM.NABERS.table_a21.building_category
        [building_type][adjustment_year_string])
        return (hist_rating + annual_rating_adj * (cur_year - hist_year))


class ESS__NABERS_no_more_than_7_years_between_current_year_and_historical_rating_date(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.4 (a)"
    label = 'Is the Historical Baseline NABERS Rating calculated no more than 7 years' \
            ' before the end date of the Current Rating Year?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS Historical Baseline NABERS Rating No More Than 7 Years Before Current Rating Year",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        end_date_of_current_NABERS_rating_period = buildings('ESS__NABERS_end_date_of_current_NABERS_rating_period', period)
        end_date_of_historical_NABERS_rating_period = buildings('ESS__NABERS_end_date_of_historical_NABERS_rating_period', period)
        current_rating_year = end_date_of_current_NABERS_rating_period.astype('datetime64[Y]')
        end_date_of_current_rating_year = (current_rating_year + np.timedelta64(11, 'M') + np.timedelta64(30, 'D')).astype('datetime64[D]')
        number_of_years_between_historical_end_date_and_end_of_current_year = ((end_date_of_current_rating_year
                                                                                - end_date_of_historical_NABERS_rating_period).astype('int')
                                                                                ).astype('datetime64[D]').astype('datetime64[Y]').astype('int')
        maximum_number_of_years_between_historical_and_current = parameters(period).ESS.MBM.NABERS.NABERS_related_constants.years_between_historical_and_current_rating
        return number_of_years_between_historical_end_date_and_end_of_current_year <= maximum_number_of_years_between_historical_and_current


class ESS__NABERS_historical_rating_meets_similar_configuration_criteria(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.4 (c)"
    label = 'Does the Historical Rating meet the similar configuration criteria, as defined' \
            ' in the NABERS Baseline Method Guide?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Historical Rating Meets Similar Configuration Criteria",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_is_eligible_for_method_two(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.3"
    label = 'Is the user eligible to use Method 2?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS User is Eligible for Calculation Method 2",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        eligible_for_method_one = buildings('ESS__NABERS_is_eligible_for_method_one', period)
        exceeds_benchmark_rating = buildings('ESS__NABERS_current_star_rating_exceeds_method_two_benchmark_rating', period)
        no_more_than_7_years_between_ratings = buildings('ESS__NABERS_no_more_than_7_years_between_current_year_and_historical_rating_date', period)
        meets_similar_configuration_criteria = buildings('ESS__NABERS_historical_rating_meets_similar_configuration_criteria', period)
        return (np.logical_not(eligible_for_method_one) * exceeds_benchmark_rating
                * no_more_than_7_years_between_ratings * meets_similar_configuration_criteria)


class ESS__NABERS_implementation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.5"
    label = 'What is the Implementation Date of the NABERS Rating? Note, the' \
            ' Implementation Date is the end date of the first Rating Period for' \
            ' which Energy Savings will be calculated.'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS Implementation Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        current_rating_end_date = buildings('ESS__NABERS_end_date_of_current_NABERS_rating_period', period)
        return current_rating_end_date


class ESS__NABERS_name_of_energy_saver(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.6"
    label = 'Who is the Energy Saver for the Implementation? This is defined as' \
            ' the person whose name is identified on the NABERS Rating Certificate,' \
            ' or if this is not present, the building owner or manager of the buildings' \
            ' identified on the NABERS Rating Certificate.'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS Energy Saver",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_energy_savings_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.7"
    label = 'What is the date on which Energy Savings occurred? This is the date' \
            ' that the Scheme Administrator determines the relevant NABERS Rating' \
            ' was completed.'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS Energy Savings Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        current_rating_end_date = buildings('ESS__NABERS_end_date_of_current_NABERS_rating_period', period)
        return current_rating_end_date


class ESS__NABERS_ESC_creation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.8"
    label = 'What is the date on which ESCs are registered and created?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS ESC Creation Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_current_rating_period_length(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.8"
    label = 'What is the length of the Current NABERS Rating Period, as' \
            ' using the current start date and current end date?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS ESC Creation Date",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        start_date = (buildings(
            'ESS__NABERS_end_date_of_current_NABERS_rating_period', period
            ))
        end_date = (buildings(
            'ESS__NABERS_ESC_creation_date', period
            ))
        rating_period_length = np.fromiter(map(count_months, start_date, end_date), int)
        return rating_period_length
        # need to troubleshoot this later


class ESS__NABERS_TypeOfCreation(Enum):
    annual_creation = 'The ESCS will be annually created.'
    forward_creation = 'The ESCS will be forward created.'


class ESS__NABERS_type_of_creation(Variable):
    value_type = Enum
    possible_values = ESS__NABERS_TypeOfCreation
    default_value = ESS__NABERS_TypeOfCreation.annual_creation
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8"
    label = 'Do you want to annually create or forward create ESCs?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Type of Creation",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_previous_forward_creation_occurred(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.3 (a) (ii)"
    label="Has forward creation for ESCs within the ESS previously occurred for this building?"
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Has Previous Forward Creation Occurred",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_forward_creation_within_15_months(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.10 (b)"
    label = 'Is the Historical Baseline NABERS Rating within 15 months of the end' \
            ' date of the Current NABERS Rating?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS Forward Creation Within 15 Months",
        "major-cat":"Energy Savings Scheme",
        "monor-cat":'Metered Baseline Method - NABERS baseline'
        }

    def formula(buildings, period, parameters):
        start_date = (buildings(
            'ESS__NABERS_end_date_of_historical_NABERS_rating_period', period
            ))
        end_date = (buildings(
            'ESS__NABERS_end_date_of_current_NABERS_rating_period', period
            ))
        rating_period_length = np.fromiter(map(count_months, start_date, end_date), int)
        return rating_period_length <= 15


class ESS__NABERS_historical_rating_previously_used_to_set_baseline(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.10 (c)"
    label = 'Has the Historical Baseline NABERS Rating, or a rating of the same' \
            ' or lower star rating value, been previously used to set a Historical' \
            ' NABERS Baseline Rating?'
    metadata={
        "variable-type": "user-input",
        "alias":"NABERS Previous or Equal Historical NABERS Rating",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }


class ESS__NABERS_ESC_creation_less_than_7_years_after_historical_rating_date(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.11 (b)"
    label = 'Is the ESC creation date no later than 7 years after the end of' \
            ' the Historical Baseline NABERS Rating?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS ESC Creation Within 7 Years of Historical Rating",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        end_date_historical_rating_period = buildings('ESS__NABERS_end_date_of_historical_NABERS_rating_period', period)
        ESC_creation_date = buildings('ESS__NABERS_ESC_creation_date', period)
        distance_between_in_years = (ESC_creation_date - end_date_historical_rating_period).astype('datetime64[Y]').astype('int')
        return distance_between_in_years <= 7


class ESS__NABERS_is_eligible_for_forward_creation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.10"
    label = 'Is the user eligible to use the annual creation method?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"NABERS Is Eligible To Forward Create ESCs",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        eligible_for_method_one = buildings('ESS__NABERS_is_eligible_for_method_one', period)
        eligible_for_method_two = buildings('ESS__NABERS_is_eligible_for_method_two', period)
        previous_forward_creation = buildings('ESS__NABERS_previous_forward_creation_occurred', period)
        forward_creation_within_15_months = buildings('ESS__NABERS_forward_creation_within_15_months', period)
        ESCs_within_7_years = buildings('ESS__NABERS_ESC_creation_less_than_7_years_after_historical_rating_date', period)
        return (np.logical_not(eligible_for_method_one)
                * (eligible_for_method_two * np.logical_not(previous_forward_creation)
                   * forward_creation_within_15_months * ESCs_within_7_years))


class ESS__NABERS_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    reference="Clause 8.8.10 (c)"
    label = 'Is the user eligible to create ESCs within the NABERS method?'
    metadata={
        "variable-type": "output",
        "alias":"NABERS Eligible to Create ESCs",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Metered Baseline Method - NABERS baseline'
        "regulation_reference": ESS_2021["8","8"]
        }

    def formula(buildings, period, parameters):
        uses_NABERS_rating_tool = buildings('ESS__NABERS_rating_calculated_using_NABERS_rating_tools', period)
        has_GreenPower = buildings('ESS__NABERS_building_has_GreenPower', period)
        on_site_generation_identified = buildings('ESS__NABERS_all_sources_of_on_site_electricity_generation_identified', period)
        unaccounted_electricity_metered_and_recorded = buildings('ESS__NABERS_on_site_unaccounted_electricity_metered_and_recorded', period)
        eligible_for_method_one = buildings('ESS__NABERS_is_eligible_for_method_one', period)
        meets_overall_NABERS_requirements = (uses_NABERS_rating_tool
                                            * (np.logical_not(has_GreenPower)) * on_site_generation_identified
                                            * unaccounted_electricity_metered_and_recorded)
        eligible_for_method_one = buildings('ESS__NABERS_is_eligible_for_method_one', period)
        return (meets_overall_NABERS_requirements * (eligible_for_method_one))
