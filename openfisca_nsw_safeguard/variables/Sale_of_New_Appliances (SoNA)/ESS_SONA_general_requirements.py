from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from datetime import date

class ESS__SONA_activity_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible for the SONA method?' 
    metadata = {
        "variable-type": "inter-interesting",
        'alias': "SONA Activity is Eligible",
    }

    def formula(buildings, period, parameters):
        meets_equipment_requirements = buildings(
          'ESS__SONA_meets_all_equipment_requirements', period
        )
        sold_by_appliance_retailer = buildings(
          'ESS__SONA_equipment_is_sold_by_appliance_retailer', period
        )
        new_at_time_of_sale = buildings(
          'ESS__SONA_equipment_new_at_time_of_sale', period
        )
        is_delivered_to_address = buildings(
          'ESS__SONA_equipment_is_delivered_to_address', period
        )
        sold_with_recorded_address = buildings(
          'ESS__SONA_equipment_sold_with_recorded_address', period
        )
        has_acceptable_evidence = buildings(
          'ESS__SONA_has_acceptable_evidence', period
        )

        is_eligible = (
          meets_equipment_requirements *
          sold_by_appliance_retailer *
          new_at_time_of_sale *
          (is_delivered_to_address + sold_with_recorded_address) *
          has_acceptable_evidence
        )

        return is_eligible


class ESS__SONA_meets_all_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the item of End-User Equipment meet the Equipment Requirements' \
            ' of its relevant Activity Definition?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (a) - Sale of New Appliances.'
    #  need to build in logic for pulling the relevant activity definitions


class ESS__SONA_equipment_is_sold_by_appliance_retailer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is each item of End-User Equipment sold by a Retailer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (b) - Sale of New Appliances.'


class ESS__SONA_equipment_retailer(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'What is the name of the retailer who sold the end user equipment?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (b) - Sale of New Appliances.'


class ESS__SONA_equipment_new_at_time_of_sale(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is each item of End-User Equipment new at the time it was sold' \
            ' by a Retailer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (c) - Sale of New Appliances.'


class ESS__SONA_equipment_is_delivered_to_address(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is each item of End-User Equipment delivered to an Address?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (d) - Sale of New Appliances.'


class ESS__SONA_equipment_sold_with_recorded_address(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is each item of End-User Equipment sold with a recorded Address?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (d) - Sale of New Appliances.'


class ESS__SONA_delivery_or_sold_address_recorded(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is each item of End-User Equipment sold with a recorded Address?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (d) - Sale of New Appliances.'
    #  a way you could operationalise this is by requiring the Address variable, \
    #  below, to be more than zero - but note it doesn't require the Address to be \
    #  recorded if it's delivered.

    def formula(buildings, period, parameters):
        delivered_to_address = buildings('equipment_is_delivered_to_address', period)
        sold_with_recorded_address = buildings('equipment_sold_with_recorded_address', period)
        return delivered_to_address + sold_with_recorded_address


class ESS__SONA_delivery_or_purchaser_address(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'What is the address the End User Equipment is being delivered to,' \
            ' or if it is not being delivered, the Address of the Purchaser' \
            ' of the Equipment?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (d) - Sale of New Appliances.'
    #  a way you could operationalise this is by requiring the Address variable, \
    #  below, to be more than zero - but note it doesn't require the Address to be \
    #  recorded if it's delivered.


class ESS__SONA_has_acceptable_evidence(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Implementation has appropriate evidence, such as a tax receipt or other acceptable evidence?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.5 - Sale of New Appliances.'

    def formula(buildings, period, parameters):
        retailer = buildings('equipment_retailer', period)
        return retailer


class ESS__SONA_date_of_sale(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the date at which the new End User Equipment was sold?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.2 - Sale of New Appliances.'


class ESS__SONA_implementation_site(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'What is the site of the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.3 - Sale of New Appliances.'

    def formula(buildings, period, parameters):
        delivery_or_purchaser_address = buildings('delivery_or_purchaser_address', period)
        return delivery_or_purchaser_address


class ESS__SONA_installation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Installation Date of the End User Equipment?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.4 - Sale of New Appliances.'

    def formula(buildings, period, parameters):
        date_of_sale = buildings('ESS__SONA_date_of_sale', period)
        return date_of_sale


class ESS__SONA_energy_saver(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Who is the Energy Saver for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.5 - Sale of New Appliances.'

    def formula(buildings, period, parameters):
        retailer = buildings('equipment_retailer', period)
        return retailer
