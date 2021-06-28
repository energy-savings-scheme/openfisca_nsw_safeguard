from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from datetime import date

class ESS__HEER_activity_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the HEER activity eligible within the ESS?'
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Activity is Eligible",
    }

    def formula(buildings, period, parameters):
        site_is_residential_or_small_business = buildings(
        'ESS__HEER_site_is_residential_or_small_business', period)
        site_assessment_conducted_before_implementation_date = buildings(
        'ESS__HEER_site_assessment_conducted_before_implementation_date', period)
        activity_eligibility_requirements_are_met = buildings(
        'ESS__HEER_activity_eligibiity_requirements_are_met', period)
        products_meet_equipment_requirements = buildings(
        'ESS__HEER_installed_equipment_or_modified_products_meet_equipment_requirements', period)
        implementation_meets_implementation_requirements = buildings(
        'ESS__HEER_implementation_meets_implementation_requirements', period)
        minimum_contribution_is_paid_or_exempt = buildings(
        'ESS__HEER_purchaser_has_paid_minimum_contribution_or_is_exempt', period)
        is_eligible = (
          site_is_residential_or_small_business * 
          site_assessment_conducted_before_implementation_date *
          activity_eligibility_requirements_are_met * 
          products_meet_equipment_requirements * 
          implementation_meets_implementation_requirements * 
          minimum_contribution_is_paid_or_exempt
        )
        return is_eligible


class ESS__HEER_site_is_residential_or_small_business(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the site a Residential or Small Business Site?'
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Implementation is at Residential or Small Business Site",
    }
    # need to build building type enum and link it to this


class ESS__HEER_site_assessment_conducted_before_implementation_date(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has a Site Assessment been conducted on or before the' \
            ' Implementation Date?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (b) - Home Energy Efficiency Retrofits.'

    def formula(buildings, period, parameters):
        implementation_date = buildings('ESS__HEER_site_implementation_date', period)
        site_assessment_date = buildings('ESS__HEER_site_assessment_date', period)
        return site_assessment_date < implementation_date


class ESS__HEER_site_assessment_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Site Assessment Date for the Energy Savings Activity?'
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Site Assessment Date",
    }


class ESS__HEER_site_implementation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Site Implementation Date for the Energy Savings Activity?'
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Site Implementation Date",
    }


class ESS__HEER_activity_eligibiity_requirements_are_met(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Have all of the Eligibility Requirements for the relevant' \
            ' Activity Definition been met immediately prior to the' \
            ' Implementation Date?'  # what does "immediately prior" mean? \
    # do we need a "date that requirements are met" variable?
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Activity Eligibility Requirements Are Met",
    }


class ESS__HEER_installed_equipment_or_modified_products_meet_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Have all of the Equipment Requirements for the Activity Definition' \
            ' been met by the installed End User Equipment or products which' \
            ' modify existing End User Equipment?'  # need to build in logic \
    # which applies this only to RESAs which install new equipment \
    # or modify existing equipment?
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Installed Equipment Meets Equipment Requirements",
    }


class ESS__HEER_implementation_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Implementation meet all of the Implementation' \
            ' Requirements for the relevant activity?'
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Implementation Meets Implementation Requirements",
    }


class ESS__HEER_purchaser_has_paid_minimum_contribution_or_is_exempt(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the Purchaser paid a net amount of minimum of $30 for the' \
            ' Implementation, or are they exempt?'
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Purchaser Has Paid Minimum Contribution Or Is Exempt",
    }

    def formula(buildings, period, parameters):
        paid_minimum_contribution = buildings('ESS__HEER_purchaser_paid_minimum_contribution', period)
        low_income_program = buildings('ESS__HEER_activity_delivered_through_low_income_program', period)
        exempt_energy_program = buildings('ESS__HEER_activity_delivered_through_exempt_energy_program', period)
        return paid_minimum_contribution + low_income_program + exempt_energy_program


class ESS__HEER_purchaser_paid_minimum_contribution(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the Purchaser paid a net amount of minimum of $30 for the' \
            ' Implementation?'
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Purchaser Has Paid Minimum Contribution",
    }


class ESS__HEER_activity_delivered_through_low_income_program(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Implementation delivered through a Low-income Energy Program?'
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Activity Delivered Through Low-Income Energy Program",
    }


class ESS__HEER_activity_delivered_through_exempt_energy_program(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Implementation delivered through an Exempt Energy Program?'
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Activity Delivered Through Exempt Energy Program",
    }


class ESS__HEER_energy_saver(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Who is the Energy Saver for the Implementation? The Energy Saver' \
            ' for Home Energy Efficiency Retrofits is the Purchaser.'
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Energy Saver",
    }

    def formula(buildings, period, parameters):
        purchaser = buildings('ESS__HEER_purchaser', period)
        return purchaser


class ESS__HEER_purchaser(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Who is the Purchaser for the Implementation?'
    metadata = {
        "variable-type": "user-input",
        'alias': "HEER Purchaser",
    }
