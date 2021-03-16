# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class meets_all_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the item of End-User Equipment meet the Equipment Requirements' \
            ' of its relevant Activity Definition?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (a) - Sale of New Appliances.'
    #  need to build in logic for pulling the relevant activity definitions

    def formula(buildings, period, parameters):
        activity_definition = buildings('SONA_activity_definition', period)
        B1_activity = (activity_definition == SONAActivityDefinition.B1)
        B2_activity = (activity_definition == SONAActivityDefinition.B2)
        B3_activity = (activity_definition == SONAActivityDefinition.B3)
        B4_activity = (activity_definition == SONAActivityDefinition.B4)
        B5_activity = (activity_definition == SONAActivityDefinition.B5)
        B6_activity = (activity_definition == SONAActivityDefinition.B6)
        B7_activity = (activity_definition == SONAActivityDefinition.B7)
        B1_equipment_requirements = buildings('B1_meets_all_equipment_requirements', period)
        B2_equipment_requirements = buildings('B2_meets_all_equipment_requirements', period)
        B3_equipment_requirements = buildings('B3_meets_all_equipment_requirements', period)
        B4_equipment_requirements = buildings('B4_meets_all_equipment_requirements', period)
        B5_equipment_requirements = buildings('B5_meets_all_equipment_requirements', period)
        B6_equipment_requirements = buildings('B6_meets_all_equipment_requirements', period)
        B7_equipment_requirements = buildings('B7_meets_all_equipment_requirements', period)
        equipment_requirements = select([B1_activity, B2_activity, B3_activity,
        B4_activity, B5_activity, B6_activity, B7_activity],
        [B1_equipment_requirements, B2_equipment_requirements,
         B3_equipment_requirements, B4_equipment_requirements,
         B5_equipment_requirements, B6_equipment_requirements,
         B7_equipment_requirements])
        return equipment_requirements


class equipment_is_sold_by_appliance_retailer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is each item of End-User Equipment sold by a Retailer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (b) - Sale of New Appliances.'


class equipment_retailer(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'What is the name of the retailer who sold the end user equipment?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (b) - Sale of New Appliances.'


class equipment_new_at_time_of_sale(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is each item of End-User Equipment new at the time it was sold' \
            ' by a Retailer?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (c) - Sale of New Appliances.'


class equipment_is_delivered_to_address(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is each item of End-User Equipment delivered to an Address?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (d) - Sale of New Appliances.'


class equipment_sold_with_recorded_address(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is each item of End-User Equipment sold with a recorded Address?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.1 (d) - Sale of New Appliances.'


class delivery_or_sold_address_recorded(Variable):
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


class delivery_or_purchaser_address(Variable):
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


class date_of_sale(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the date at which the new End User Equipment was sold?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.2 - Sale of New Appliances.'


class implementation_site(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'What is the site of the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.3 - Sale of New Appliances.'

    def formula(buildings, period, parameters):
        delivery_or_purchaser_address = buildings('delivery_or_purchaser_address', period)
        return delivery_or_purchaser_address


class SONA_installation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Installation Date of the End User Equipment?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.4 - Sale of New Appliances.'

    def formula(buildings, period, parameters):
        date_of_sale = buildings('date_of_sale', period)
        return date_of_sale


class SONA_energy_saver(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'Who is the Energy Saver for the Implementation?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 9.3.5 - Sale of New Appliances.'

    def formula(buildings, period, parameters):
        retailer = buildings('equipment_retailer', period)
        return retailer


class SONAActivityDefinition(Enum):
    B1 = "Activity Definition B1"
    B2 = "Activity Definition B2"
    B3 = "Activity Definition B3"
    B4 = "Activity Definition B4"
    B5 = "Activity Definition B5"
    B6 = "Activity Definition B6"
    B7 = "Activity Definition B7"


class SONA_activity_definition(Variable):
    value_type = Enum
    entity = Building
    possible_values = SONAActivityDefinition
    default_value = SONAActivityDefinition.B1
    definition_period = ETERNITY
    label = 'What is the Activity Definition that Energy Savings are being' \
            ' created for?'
