# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class site_is_residential_or_small_business(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the site a Residential or Small Business Site?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (a) - Home Energy Efficiency Retrofits.'

    def formula(buildings, period, parameters):
        building_type = buildings('building_type', period)
        BuildingType = building_type.possible_values
        is_residential = (building_type == BuildingType.residential_building)
        is_small_business = (building_type == BuildingType.small_business_site)
        return is_residential + is_small_business


class site_assessment_conducted_before_implementation_date(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has a Site Assessment been conducted on or before the' \
            ' Implementation Date?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (b) - Home Energy Efficiency Retrofits.'

    def formula(buildings, period, parameters):
        implementation_date = buildings('implementation_date', period)
        site_assessment_date = buildings('site_assessment_date', period)
        return site_assessment_date >= implementation_date


class site_implementation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Site Assessment Date for the RESA?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (b) - Home Energy Efficiency Retrofits.'


class eligibiity_requirements_are_met(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Have all of the Eligibility Requirements for the relevant' \
            ' Activity Definition been met immediately prior to the' \
            ' Implementation Date?'  # what does "immediately prior" mean? \
    # do we need a "date that requirements are met" variable?
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (c) - Home Energy Efficiency Retrofits.'


class installed_equipment_or_modified_products_meet_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Have all of the Equipment Requirements for the Activity Definition' \
            ' been met by the installed End User Equipment or products which' \
            ' modify existing End User Equipment?'  # need to build in logic \
    # which applies this only to RESAs which install new equipment \
    # or modify existing equipment?
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (d) - Home Energy Efficiency Retrofits.'


class implementation_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Implementation meet all of the Implementation' \
            ' Requirements for the relevant activity?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (e) - Home Energy Efficiency Retrofits.'


class purchaser_has_paid_minimum_contribution_or_is_exempt(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the Purchaser paid a net amount of minimum of $30 for the' \
            ' Implementation, or are they exempt?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (f) - Home Energy Efficiency Retrofits.'

    def formula(buildings, period, parameters):
        paid_minimum_contribution = buildings('purchaser_paid_minimum_contribution', period)
        low_income_program = buildings('activity_delivered_through_low_income_program', period)
        exempt_energy_program = buildings('activity_delivered_through_exempt_energy_program', period)
        return paid_minimum_contribution + low_income_program + exempt_energy_program


class purchaser_paid_minimum_contribution(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the Purchaser paid a net amount of minimum of $30 for the' \
            ' Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (f) - Home Energy Efficiency Retrofits.'


class activity_delivered_through_low_income_program(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Implementation delivered through a Low-income Energy Program?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (f) - Home Energy Efficiency Retrofits.'


class activity_delivered_through_exempt_energy_program(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Implementation delivered through an Exempt Energy Program?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (f) - Home Energy Efficiency Retrofits.'


class heer_energy_saver(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Who is the Energy Saver for the Implementation? The Energy Saver' \
            ' for Home Energy Efficiency Retrofits is the Purchaser.'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8.3 - Home Energy Efficiency Retrofits.'

    def formula(buildings, period, parameters):
        purchaser = buildings('heer_purchaser', period)
        return purchaser


class heer_purchaser(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Who is the Purchaser for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8.3 - Home Energy Efficiency Retrofits.'
