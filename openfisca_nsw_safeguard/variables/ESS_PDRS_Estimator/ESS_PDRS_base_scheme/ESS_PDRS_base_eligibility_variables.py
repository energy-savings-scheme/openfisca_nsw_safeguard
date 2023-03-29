import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
from datetime import date


class Base_reduces_energy_consumption(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Does the activity reduce energy consumption compared to what would have been consumed?',
        'sorting' : 1,
        'eligibility_clause' : """In ESS Clause 5.3 it states that a Recognised Energy Saving Activity is any activity that meets all of the following criteria: <br />
        (a) it increases the efficiency of energy consumption, by: <br />
        (i) modifying End-User Equipment or the usage of End-User Equipment (including by installing additional components) with the result that there is a reduction in the
        consumption of energy compared to what would have otherwise been consumed;<br />
        (ii) replacing End-User Equipment with other End-User Equipment that consumes less energy, subject to clause 5.3A;<br />
        (iii) installing New End-User Equipment that consumes less energy than other comparable End-User Equipment of the same type, function, output or service, subject to clause
        5.3B; or <br />
        (iv) removing End-User Equipment with the result that there is a reduction in the consumption of energy compared to what would have otherwise been consumed,
        subject to clause 5.3A."""
    }


class Base_provides_capacity_to_reduce_demand(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        # 'label' : 'The Peak Demand Reduction period is 2.30pm to 8.30pm AEST',
        'display_question' : 'Does the activity provide capacity to reduce demand during the Peak Demand Reduction period?',
        'sorting' : 2,
        'eligibility_clause' : """ In PDRS Clause 5.1 it states a Recognised Peak Activity is an activity that:<br />
        (a) provides capacity to reduce peak demand during the Peak Demand Reduction Period."""
    }


class Base_implemented_activity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has implementation already occurred?',
        'sorting' : 3,
        'eligibility_clause' : """In ESS Clause 5.3A(b) it states that the replacement or removal of End-User Equipment only constitutes a Recognised Energy Saving Activity if the Implementation Date is on or after 15 May 2016, disposes of that End-User Equipment appropriately.<br /> 
                                  In PDRS Clause5.1(d), it states that a Recognised Peak Activity is an activity that has an Implementation Date on or after 1 April 2022."""
    }


class implementation_date_options(Enum):
    planned_activity        = 'Planned activity'        #not eligible
    before_april_1_2022     = 'Before 1 April 2022'     #not eligible
    april_1_2022_or_later   = '1 April 2022 or later'   #ESCs and PRCs 


class Implementation_date(Variable):
    value_type = Enum
    entity = Building
    possible_values = implementation_date_options
    default_value = implementation_date_options.planned_activity
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'What date did the implementation occur?',
        'sorting' : 4,
        'eligibility_clause' : """In PDRS Clause5.1(d), it states that a Recognised Peak Activity is an activity that has an Implementation Date on or after 1 April 2022."""
    }


class Implementation_date_eligibility(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):

        implementation_date = buildings('Implementation_date', period)
        return np.select(
            [
                implementation_date == implementation_date_options.planned_activity,
                implementation_date == implementation_date_options.before_april_1_2022,
                implementation_date == implementation_date_options.april_1_2022_or_later
            ],
            [
                False,
                False,
                True
            ])


class Base_lawful_activity(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Was the activity lawful in NSW on the implementation date?',
        'sorting' : 5,
        'eligibility_clause' : """In PDRS Clause 5.1(c) it states that a Recognised Peak Activity is an activity that is not unlawful in New South Wales on the Implementation Date."""
    }


class Base_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Was or will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 6,
        'eligibility_clause' : """In ESS Clause 6.2 it states that an Accredited Certificate Provider may only create Energy Savings Certificates in respect of the Energy Savings for an Implementation where:<br />
                                  (a) the Accredited Certificate Provider is the Energy Saver for those Energy Savings as at the Implementation Date; and <br />
                                  (b) the Accredited Certificate Provider’s Accreditation Date for that Recognised Energy Saving Activity is prior to the Implementation Date."""
    }


class Base_removing_or_replacing(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the activity removing or replacing End-User equipment?',
        'sorting' : 7,
        'eligibility_clause' : """In ESS Clause 5.3 it states that a Recognised Energy Saving Activity is any activity that meets all of the following criteria: <br />
        (a) it increases the efficiency of energy consumption, by: <br />
        (i) modifying End-User Equipment or the usage of End-User Equipment (including by installing additional components) with the result that there is a reduction in the
        consumption of energy compared to what would have otherwise been consumed;<br />
        (ii) replacing End-User Equipment with other End-User Equipment that consumes less energy, subject to clause 5.3A;<br />
        (iii) installing New End-User Equipment that consumes less energy than other comparable End-User Equipment of the same type, function, output or service, subject to clause
        5.3B; or <br />
        (iv) removing End-User Equipment with the result that there is a reduction in the consumption of energy compared to what would have otherwise been consumed,
        subject to clause 5.3A."""
    }


class Base_disposal_of_equipment(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the End-User equipment be disposed of in accordance with legal requirements, (including by obtaining evidence for any refrigerants being disposed of or recycled)?',
        'sorting' : 8,
        'conditional': 'True',
        'eligibility_clause' : """In PDRS Clause 5.3(b) it states that the replacement or removal of End-User Equipment only constitutes a Recognised Peak Activity if it is disposed of in accordance with legal requirements imposed through a statutory or regulatory instrument of the Commonwealth or a State or Territory of the Commonwealth, including by obtaining evidence for any refrigerants being disposed of or recycled."""
    }


class Base_resold_reused_or_refurbished(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the removed End-User equipment re-sold, refurbished or re-used?',
        'sorting' : 9,
        'conditional' : 'True',
        'eligibility_clause' : """In PDRS Clause 5.3(a) it states that the replacement or removal of End-User Equipment only constitutes a Recognised Peak Activity if the End-User Equipment is not refurbished, re-used or resold."""
    }


class Base_reduces_safety_levels(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the activity reduce safety levels or permanently reduce production or service levels?',
        'sorting' : 10,
        'eligibility_clause' : """In PDRS Clause 5.4(a) it states that an activity is not a Recognised Peak Activity if it results in the creation
        of Peak Demand Reduction Capacity by reducing safety levels or permanently reducing production or service levels."""
    }


class Base_greenhouse_emissions_increase(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Will the activity lead to a net increase in greenhouse emissions?',
        'sorting' : 11,
        'eligibility_clause' : """In PDRS Clause 5.4(b) it states that an activity is not a Recognised Peak Activity if it contributes to a net increase in greenhouse gas emissions."""
    }


class Base_meets_mandatory_requirement(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Is the activity being undertaken to comply with any mandatory legal requirements?',
        'sorting' : 12,
        'eligibility_clause' : """In PDRS Clause 5.4(c) it states that an activity is not a Recognised Peak Activity if it is undertaken to comply with any mandatory legal requirement imposed through a statutory or regulatory instrument of the Commonwealth or a State or Territory of the Commonwealth, including but not limited to National Construction Code and BASIX affected development requirements, except for alterations, enlargements or extensions of a BASIX affected development as defined in clause 3(1)(c) of the Environmental Planning and Assessment Regulation 2021."""
    }


class Base_basix_affected_development(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Is the activity an alteration, enlargement or extension of a BASIX affected development?',
        'sorting' : 13,
        'conditional': 'True',
        'eligibility_clause' : """In PDRS Clause 5.4(c) it states that an activity is not a Recognised Peak Activity if it is undertaken to comply with any mandatory legal requirement imposed through a statutory or regulatory instrument of the Commonwealth or a State or Territory of the Commonwealth, including but not limited to National Construction Code and BASIX affected development requirements, except for alterations, enlargements or extensions of a BASIX affected development as defined in clause 3(1)(c) of the Environmental Planning and Assessment Regulation 2021."""
    }


class Base_prescribed_transmission_service(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
        'display_question': 'Is the activity a Standard Control Service or Prescribed Transmission service undertaken by a Network Service Provider?',
        'sorting' : 14,
        'eligibility_clause' : """In PDRS Clause 5.4(d) it states that an activity is not a Recognised Peak Activity if it is a Standard Control Service or Prescribed Transmission Service undertaken by a Network Service Provider in accordance with the National Electricity Rules under the National Electricity (NSW) Law, except if the activity is a Non-Network Option."""
    }


class Base_tradeable_certificates(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the activity eligible to create tradeable certificates under the Renewable Energy Act?',
        'sorting' : 15,
        'eligibility_clause' : """In PDRS Clause 5.4(e) it states that an activity is not a Recognised Peak Activity if it is eligible to create tradeable certificates under the Renewable Energy (Electricity) Act 2000 (Cth), except if the activity is the installation of a replacement heat pump water heater."""
    }


class Base_replacement_water_heater_certificates(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the activity the installation of a replacement heat pump water heater?',
        'sorting' : 16,
        'conditional': 'True',
        'eligibility_clause' : """In PDRS Clause 5.4(e) it states that an activity is not a Recognised Peak Activity if it is eligible to create tradeable certificates under the Renewable Energy (Electricity) Act 2000 (Cth), except if the activity is the installation of a replacement heat pump water heater."""
    }


class Base_replacement_solar_water_heater_certificates(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the activity the installation of a replacement solar water heater?',
        'sorting' : 17,
        'conditional': 'True',
        'eligibility_clause' : """In ESS Clause 5.4(g) it states that Recognised Energy Saving Activities do not include any of the following:<br />
        an activity that is eligible to create tradeable certificates under the Renewable Energy (Electricity) Act 2000 (Cth), except if the activity is the installation of a new or replacement solar water heater or heat pump water heater."""
    }
