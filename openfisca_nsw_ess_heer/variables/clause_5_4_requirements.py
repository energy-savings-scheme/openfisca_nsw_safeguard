# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class placeholder_5_4(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Equation 1 of the ESS Rule 2009, used to calculate the number' \
            ' of ESCs generated from a Recognised Energy Savings Activity.' \
            ' As defined in Clause 6.5 of the ESS Rule 2009.'


class T5_adaptor_kits_are_ineligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a T5 Adaptor Kit, as defined' \
            ' in Table A9.3? T5 Adaptor Kits are not eligible to create ESCs.'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (a) (i) - Activities which are not Recognised' \
                ' Energy Saving Activities.'

    def formula(buildings, period, parameters):
        new_lamp_type = buildings('new_lamp_type', period)
        EquipmentClassStatus = new_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_T5_adaptor_kit = (new_lamp_type == EquipmentClassStatus.T5_adaptor_kit)
        return not(is_T5_adaptor_kit)


class retrofit_LED_linear_lamps_are_ineligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a Retrofit Luminaire LED Linear' \
            ' Lamp, as defined in Table A9.3? Retrofit Luminaire LED Linear' \
            ' Lamps are not eligible to create ESCs.'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (a) (ii) - Activities which are not Recognised' \
                ' Energy Saving Activities.'

    def formula(buildings, period, parameters):
        new_lamp_type = buildings('new_lamp_type', period)
        EquipmentClassStatus = new_lamp_type.possible_values  # imports functionality of Table A9.1 and Table A9.3 to define existing lamp type
        is_T5_adaptor_kit = (new_lamp_type == EquipmentClassStatus.retrofit_luminaire_LED_linear_lamp)
        return not(is_T5_adaptor_kit)


class activity_required_to_comply_with_mandatory_legal_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity undertaken to comply with a mandatory legal' \
            ' requirement imposed through a statutory or regulatory instrument' \
            ' of any jurisdiction, including BASIX and BCA requirements?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (b) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class activity_is_standard_control_service_or_prescribed_transmission_service(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a Standard Control Service or a Prescribed' \
            ' Transmission Service undertaken by a Network Service Provider?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (c) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class activity_is_supply_purchase_from_retailer_for_emissions_reduction(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a purchase or supply of electricity from a retailer' \
            ' with a representation that the purchased or supplied electricity' \
            ' reduces greenhouse emissions?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (d) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class production_or_service_levels_are_reduced(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity result in a reduction of the consumption of' \
            ' energy by reducing production levels, service levels, or both?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (e) - Activities which are not Recognised' \
                ' Energy Saving Activities.'

    def formula(buildings, period, parameters):
        reduces_production_or_service_levels = buildings('activity_reduces_production_or_service_levels', period)
        return reduces_production_or_service_levels


class increases_non_renewable_fuel_consumption_for_equivalent_services(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity reduce energy consumption by increasing' \
            ' consumption of non-renewable fuels, other than Gas, to provide' \
            ' equivalent goods or services?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (f) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class is_eligible_to_create_RECs(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity eligible to create certificates under the' \
            ' Renewable Energy (Electricity) Act 2000?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (g) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class activity_flares_gas(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity result in the flaring of Gas?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (h) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class activity_exports_to_the_electricity_network(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity result in generating electricity which is'
            ' exported to the Electricity Network?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (i) (i) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class generating_system_more_than_30MW(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the generating system have a nameplate rating of 30MW or higher?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (i) (ii) - Activities which are not Recognised' \
                ' Energy Saving Activities.'

    def formula(buildings, period, parameters):
        nameplate_rating = buildings('generator_nameplate_rating', period)
        return nameplate_rating >= 30


class generator_nameplate_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the nameplate rating of the generating system, in MW?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (i) (ii) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class baseline_greenhouse_gas_emissions(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the greenhouse gas emissions prior to the commencement' \
            ' of a fuel switching activity?'  # need to determine if this is an annual, monthly, daily measurement
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (j) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class current_greenhouse_gas_emissions(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the greenhouse gas emissions following the completion' \
            ' of a fuel switching activity?'  # need to determine if this is an annual, monthly, daily measurement
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (j) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class fuel_switching_activity_leads_to_greenhouse_emissions_increase(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the fuel switching activity, implemented under clause 7A' \
            ' , 8.5, 8.6 or 8.7 lead to a net increase in greenhouse gas' \
            ' emissions'  # need to determine if this is an annual, monthly, daily measurement
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (j) - Activities which are not Recognised' \
                ' Energy Saving Activities.'

    def formula(buildings, period, parameters):
        is_fuel_switching = buildings('is_fuel_switching_activity', period)
        baseline_emissions = buildings('baseline_greenhouse_gas_emissions', period)
        current_emissions = buildings('current_greenhouse_gas_emissions', period)
        return (is_fuel_switching * (current_emissions > baseline_emissions)) + not(is_fuel_switching)


class in_ACT_and_required_to_report_under_national_schemes(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity required to report energy consumption under the' \
            ' National Greenhouse and Energy Reporting Act 2007?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (j) - Activities which are not Recognised' \
                ' Energy Saving Activities.'

    def formula(buildings, period, parameters):
        state = buildings('implementation_state', period)
        ImplementationState = state.possible_values
        in_ACT = (state == ImplementationState.ACT)
        national_greenhouse_act = buildings('required_to_report_under_national_greenhouse_act', period)
        EE_in_govt_operations = buildings('required_to_report_under_energy_efficiency_in_government_operations_policy', period)
        carbon_neutral_framework = buildings('required_to_report_under_carbon_neutral_ACT_government_framework', period)
        return (in_ACT * (national_greenhouse_act + EE_in_govt_operations + carbon_neutral_framework)) + not(in_ACT)


class required_to_report_under_national_greenhouse_act(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity required to report energy consumption under the' \
            ' National Greenhouse and Energy Reporting Act 2007?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (j) (i) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class required_to_report_under_energy_efficiency_in_government_operations_policy(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity required to report energy consumption under the' \
            ' Energy Efficiency in Government Operations Policy?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (j) (ii) - Activities which are not Recognised' \
                ' Energy Saving Activities.'


class required_to_report_under_carbon_neutral_ACT_government_framework(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity required to report energy consumption under the' \
            ' Energy Efficiency in Government Operations Policy?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.4 (j) (iii) - Activities which are not Recognised' \
                ' Energy Saving Activities.'
