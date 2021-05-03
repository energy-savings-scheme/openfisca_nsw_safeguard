from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from datetime import date


from openfisca_nsw_safeguard.regulation_reference import ESS_2021


class site_is_residential_or_small_business(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the site a Residential or Small Business Site?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (a) - Home Energy Efficiency Retrofits.'
    metadata = {
        "alias": "site is residential or small business",
        "regulation_reference": ESS_2021["9", "9.8"]
    }

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
    metadata = {
        "alias": "site assessment conducted before implementation date",
        "regulation_reference": ESS_2021["9", "9.8"]
    }

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
    metadata = {
        "alias": "**",
        "regulation_reference": ESS_2021["9", "9.8"]
    }


class purchaser_has_paid_minimum_contribution_or_is_exempt(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the Purchaser paid a net amount of minimum of $30 for the' \
            ' Implementation, or are they exempt?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (f) - Home Energy Efficiency Retrofits.'
    metadata = {
        "alias": "**",
        "regulation_reference": ESS_2021["9", "9.8"]
    }

    def formula(buildings, period, parameters):
        paid_minimum_contribution = buildings(
            'purchaser_paid_minimum_contribution', period)
        low_income_program = buildings(
            'activity_delivered_through_low_income_program', period)
        exempt_energy_program = buildings(
            'activity_delivered_through_exempt_energy_program', period)
        return paid_minimum_contribution + low_income_program + exempt_energy_program


class purchaser_paid_minimum_contribution(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the Purchaser paid a net amount of minimum of $30 for the' \
            ' Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (f) - Home Energy Efficiency Retrofits.'
    metadata = {
        "alias": "**",
        "regulation_reference": ESS_2021["9", "9.8"]
    }


class activity_delivered_through_low_income_program(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Implementation delivered through a Low-income Energy Program?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (f) - Home Energy Efficiency Retrofits.'
    metadata = {
        "alias": "**",
        "regulation_reference": ESS_2021["9", "9.8"]
    }


class activity_delivered_through_exempt_energy_program(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Implementation delivered through an Exempt Energy Program?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8 (f) - Home Energy Efficiency Retrofits.'
    metadata = {
        "alias": "**",
        "regulation_reference": ESS_2021["9", "9.8"]
    }


class heer_energy_saver(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Who is the Energy Saver for the Implementation? The Energy Saver' \
            ' for Home Energy Efficiency Retrofits is the Purchaser.'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8.3 - Home Energy Efficiency Retrofits.'
    metadata = {
        "alias": "**",
        "regulation_reference": ESS_2021["9", "9.8"]
    }

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
    metadata = {
        "alias": "**",
        "regulation_reference": ESS_2021["9", "9.8"]
    }


class meets_all_HEER_method_requirement(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Who is the Purchaser for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.8.3 - Home Energy Efficiency Retrofits.'
    metadata = {
        "alias": "**",
        "regulation_reference": ESS_2021["9", "9.8"]
    }

    def formula(buildings, period, parameters):
        req1 = buildings('site_is_residential_or_small_business', period)
        req2 = buildings(
            'site_assessment_conducted_before_implementation_date', period)
        req3 = buildings(
            'purchaser_has_paid_minimum_contribution_or_is_exempt', period)
        req4 = buildings(
            'heer_energy_saver', period)
        return req1 * req2 * req3 * req4
