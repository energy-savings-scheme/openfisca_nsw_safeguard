# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class resa_criteria_increased_efficiency(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the RESA fulfill all of the criteria required to be recongised' \
            ' as a RESA?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a)- Recognised Energy Saving Activity.'

    def formula(buildings, period, parameters):
        clause_5_3_i = buildings('modification_results_in_reduction_of_consumption', period)
        clause_5_3_ii = buildings('replacement_with_new_equipment_results_in_reduction_of_consumption', period)
        clause_5_3_iii = buildings('installed_equipment_consumes_less_energy_than_comparable_equipment', period)
        clause_5_3_iv = buildings('removed_equipment_creates_reduction_in_energy_consumption', period)
        clause_5_3_A = buildings('removal_of_equipment_meets_removal_requirements', period)
        return clause_5_3_i * clause_5_3_ii * clause_5_3_iii * clause_5_3_iv * clause_5_3_A


class modification_results_in_reduction_of_consumption(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the modification of End User Equipment result in a reduction' \
            ' in the consumption of energy, compared to what would have' \
            ' otherwise been consumed?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a) (i) - Recognised Energy Saving Activity.'

    def formula(buildings, period, parameters):
        current_consumption = buildings('current_energy_consumption', period)
        baseline_consumption = buildings('baseline_energy_consumption', period)
        return baseline_consumption > current_consumption


class replacement_with_new_equipment_results_in_reduction_of_consumption(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the replacement of existing End User Equipment with new' \
            ' End User Equipment result in a reduction in the consumption of' \
            ' energy, compared to what would have otherwise been consumed?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a) (ii) - Recognised Energy Saving Activity.'

    def formula(buildings, period, parameters):
        current_consumption = buildings('current_energy_consumption', period)
        baseline_consumption = buildings('baseline_energy_consumption', period)
        return baseline_consumption > current_consumption


class installed_equipment_consumes_less_energy_than_comparable_equipment(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the installed equipment consume less energy than a comparable' \
            ' End User Equipment of the same type, function, output or service?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a) (iii) - Recognised Energy Saving Activity.'

    def formula(buildings, period, parameters):
        current_consumption = buildings('current_energy_consumption', period)
        comparable_consumption = buildings('comparable_energy_consumption', period)
        same_type = buildings('comparable_equipment_is_same_type', period)
        same_function = buildings('comparable_equipment_is_same_function', period)
        same_output = buildings('comparable_equipment_is_same_output', period)
        same_service = buildings('comparable_equipment_is_same_service', period)
        return ((comparable_consumption > current_consumption)
        * (same_type + same_function + same_output + same_service))


class removed_equipment_creates_reduction_in_energy_consumption(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the replacement of existing End User Equipment with new' \
            ' End User Equipment result in a reduction in the consumption of' \
            ' energy, compared to what would have otherwise been consumed?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a) (iv) - Recognised Energy Saving Activity.'

    def formula(buildings, period, parameters):
        current_consumption = buildings('current_energy_consumption', period)
        baseline_consumption = buildings('baseline_energy_consumption', period)
        return baseline_consumption > current_consumption


class current_energy_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the current energy consumption following the RESA, in MWh?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a) (i) - Recognised Energy Saving Activity.'


class baseline_energy_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What was the current energy consumption prior to the RESA, in MWh?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a) (i) - Recognised Energy Saving Activity.'


class comparable_energy_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the energy consumption of comaparable equipment to' \
            ' the End User Equipment installed for to the RESA, in MWh?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a) (ii) - Recognised Energy Saving Activity.'


class activity_reduces_production_or_service_levels(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity result in a reduction in production or service' \
            ' (including safety) levels?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (b) - Recognised Energy Saving Activity.'

    def formula(buildings, period, parameters):
        reduces_production_levels = buildings('activity_reduces_production_levels', period)
        reduces_service_levels = buildings('activity_reduces_service_levels', period)
        reduces_safety_levels = buildings('activity_reduces_safety_levels', period)
        return reduces_production_levels + (reduces_service_levels * reduces_safety_levels)


class activity_reduces_production_levels(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity result in a reduction in production levels?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (b) - Recognised Energy Saving Activity.'


class activity_reduces_service_levels(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity result in a reduction in service levels?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (b) - Recognised Energy Saving Activity.'


class activity_reduces_safety_levels(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity result in a reduction in safety levels?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (b) - Recognised Energy Saving Activity.'


class site_in_ESS_jurisdiction(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Recognised Energy Savings Activity implemented in an ESS' \
            ' Jurisdiction?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (c) - Recognised Energy Saving Activity.'


class activity_is_unlawful(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the Recognised Energy Savings Activity unlawful in the ESS' \
            ' Jurisdiction as at the Implementation Date?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (d) - Recognised Energy Saving Activity.'


class activity_increases_efficiency_of_energy_consumption(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity increase the efficiency of energy consumption' \
            ' through increasing the efficiency of electricity consumption,' \
            ' increasing the efficiency of gas combusted for stationary' \
            ' energy, by fuel switching from electricity to gas or gas to' \
            ' electricity, or by generating electricity used to provide' \
            ' equivalent goods or services.'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (e) - Recognised Energy Saving Activity.'

    def formula(buildings, period, parameters):
        increases_elec_efficiency = buildings('activity_increases_efficiency_of_electricity_consumption', period)
        increases_gas_efficiency = buildings('activity_increases_efficiency_of_gas_combusted_for_stationary_energy', period)
        is_fuel_switching = buildings('is_fuel_switching_activity', period)
        elec_generation_provides_equivalent_services = buildings('electricity_generation_provides_equivalent_services', period)
        return increases_elec_efficiency * increases_gas_efficiency * is_fuel_switching * elec_generation_provides_equivalent_services


class activity_increases_efficiency_of_electricity_consumption(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity increase the efficiency of electricity consumption?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (e) (i) - Recognised Energy Saving Activity.'


class activity_increases_efficiency_of_gas_combusted_for_stationary_energy(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity increase the efficiency of gas consumption, where' \
            ' the gas is combusted for stationary energy?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (e) (ii) - Recognised Energy Saving Activity.'


class is_fuel_switching_activity(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a fuel switching activity which increases' \
            ' of energy consumption?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (e) (iii) - Recognised Energy Saving Activity.'


class electricity_generation_provides_equivalent_services(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the activity a generation activity which provides equivalent' \
            ' goods or services, with an overall redction in the consumption' \
            ' of energy compared to what otherwise would have been consumed' \
            ' subject to clause 5.4 (i)?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (e) (iv) - Recognised Energy Saving Activity.'


class does_not_refurbish_reuse_or_resell_old_equipment(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity not refurbish, reuse or resell old equipment?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3A (a) - Recognised Energy Saving Activity.'

    def formula(buildings, period, parameters):
        activity_refurbishes_equipment = buildings('removed_equipment_is_refurbished', period)
        activity_reuses_equipment = buildings('removed_equipment_is_reused', period)
        activity_resells_equipment = buildings('removed_equipment_is_resold', period)
        return not(activity_refurbishes_equipment + activity_reuses_equipment + activity_resells_equipment)


class removed_equipment_is_refurbished(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity refurbish old equipment?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3A (a) - Recognised Energy Saving Activity.'


class removed_equipment_is_reused(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity reuse old equipment?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3A (a) - Recognised Energy Saving Activity.'


class removed_equipment_is_resold(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity reuse old equipment?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3A (a) - Recognised Energy Saving Activity.'


class implementation_date(Variable):
    value_type = date
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Implementation Date for the RESA?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 10.1 - Recognised Energy Saving Activity.'


class postcode(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Postcode for the RESA?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 10.1 - Recognised Energy Saving Activity.'  # need to figure out a way to check postcode against list


class implementation_is_in_metro_levy_area(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the implementation in a Metropolitan Levy Area as listed in' \
            ' Table A25?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3A (a) - Recognised Energy Saving Activity.'

    def formula(buildings, period, parameters):
        postcode = buildings('postcode', period)
        location = parameters(period).general_ESS.table_A25
        is_urban = location.calc(postcode) == 1
        return is_urban


class lighting_mercury_is_recycled(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is any mercury contained within the old end user lighting equipment' \
            ' recycled in accordance with the recycling requirements of a' \
            ' Product Stewardship Scheme?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 10.1 - Recognised Energy Saving Activity.'
