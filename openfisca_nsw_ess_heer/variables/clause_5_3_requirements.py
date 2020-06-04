# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class RESAEfficiencyIncreaseMethod(Enum):
    modifying_end_equipment = 'Implementation increases efficiency by reducing' \
                              ' consumption of energy compared to what would have' \
                              ' otherwise been consumed, through modifying existing' \
                              ' equipment.'
    replacing_end_equipment = 'Implementation increases efficiency by reducing' \
                              ' consumption of energy compared to what would have' \
                              ' otherwise been consumed, through replacing existing' \
                              ' equipment.'
    installing_new_equipment = 'Implementation increases efficiency by reducing' \
                               ' consumption of energy compared to what would have' \
                               ' otherwise been consumed, through installing new' \
                               ' equipment which consumes less energy than' \
                               ' comparable equipment.'
    removing_end_equipment = 'Implementation increases efficiency by reducing' \
                             ' consumption of energy compared to what would have' \
                             ' otherwise been consumed, through removing existing' \
                             ' equipment.'


class resa_method(Variable):
    value_type = Enum
    possible_values = RESAEfficiencyIncreaseMethod
    default_value = RESAEfficiencyIncreaseMethod.installing_new_equipment
    entity = Building
    definition_period = ETERNITY
    label = 'What method of increasing energy efficiency does the RESA use?'


class resa_criteria_increased_efficiency(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the RESA fulfill all of the criteria required to be recongised' \
            ' as a RESA?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a)- Recognised Energy Saving Activity.'

    def formula(buildings, period, parameters):
        resa_method = buildings('resa_method', period)
        modifying_equipment = (resa_method == RESAEfficiencyIncreaseMethod.modifying_end_equipment)
        replacing_equipment = (resa_method == RESAEfficiencyIncreaseMethod.replacing_end_equipment)
        installing_equipment = (resa_method == RESAEfficiencyIncreaseMethod.installing_new_equipment)
        removing_equipment = (resa_method == RESAEfficiencyIncreaseMethod.removing_end_equipment)
        modification_creates_energy_consumption_reduction = buildings('modification_results_in_reduction_of_consumption', period)
        replacement_creates_energy_consumption_reduction = buildings('replacement_with_new_equipment_results_in_reduction_of_consumption', period)
        installation_creates_energy_consumption_reduction = buildings('installed_equipment_consumes_less_energy_than_comparable_equipment', period)
        removed_equipment_creates_reduction_in_energy_consumption = buildings('replacement_with_new_equipment_results_in_reduction_of_consumption', period)
        removal_requirements_are_met = buildings('activity_meets_removal_requirements', period)  # this is Clause 5.3A
        new_equipment_efficiency_greater_than_average = buildings('efficiency_of_new_equipment_greater_than_average_equivalent', period)
        return select([modifying_equipment,
                       replacing_equipment,
                       installing_equipment,
                       removing_equipment],
                      [modification_creates_energy_consumption_reduction,
                       (replacement_creates_energy_consumption_reduction * removal_requirements_are_met),
                       (installation_creates_energy_consumption_reduction * new_equipment_efficiency_greater_than_average),
                       (removed_equipment_creates_reduction_in_energy_consumption * removal_requirements_are_met)])


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


class comparable_equipment_is_same_type(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment the same or a comparable type as the' \
            ' existing End User Equipment, as defined by the Scheme Administrator?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a) (iv) - Recognised Energy Saving Activity.'


class comparable_equipment_is_same_function(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment provide the same or a comparable function as the' \
            ' existing End User Equipment, as defined by the Scheme Administrator?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a) (iv) - Recognised Energy Saving Activity.'


class comparable_equipment_is_same_output(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment provide the same or a comparable output as the' \
            ' existing End User Equipment, as defined by the Scheme Administrator?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a) (iv) - Recognised Energy Saving Activity.'


class comparable_equipment_is_same_service(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment provide the same or a comparable service as the' \
            ' existing End User Equipment, as defined by the Scheme Administrator?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3 (a) (iv) - Recognised Energy Saving Activity.'


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
        return increases_elec_efficiency + increases_gas_efficiency + is_fuel_switching + elec_generation_provides_equivalent_services


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


class activity_is_replacement_or_removal_of_equipment(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the act involve the replacement or removal of End-User' \
            ' Equipment, and thus require fulfilling the requirements of' \
            ' Clause 5.3A?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3A - Recognised Energy Saving Activity.'


class activity_meets_removal_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet the requirements required for removal' \
            ' activities to be defined as a RESA?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3A - Recognised Energy Saving Activity.'  # need to build \
    # in logic for lighting and refrigerant activities

    def formula(buildings, period, parameters):
        does_not_refurbish_reuse_or_resell = buildings('does_not_refurbish_reuse_or_resell_old_equipment', period)
        metro_lighting_activity_recycles_mercury = buildings('implementation_is_metro_and_lighting_mercury_is_recycled', period)
        refrigerants_are_recycled = buildings('evidence_obtained_for_refrigerant_disposal', period)
        return does_not_refurbish_reuse_or_resell * metro_lighting_activity_recycles_mercury * refrigerants_are_recycled


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


class implementation_is_metro_and_lighting_mercury_is_recycled(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the implementation is in a Metropolitan Levy Area, and the old' \
            ' End User Equipment is lighting, has the mercury contained within' \
            ' this old equipment, if any, been recycled according to the' \
            ' Recycling Requirements of a Product Stewardship Scheme?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3A (a) - Recognised Energy Saving Activity.'

    def formula(buildings, period, parameters):
        in_metro = buildings('implementation_is_in_metro_levy_area', period)
        mercury_is_recycled = buildings('lighting_mercury_is_recycled', period)
        return (in_metro * mercury_is_recycled) + (not(in_metro))  # note that if the implementation is not in metro, this condition is automatically true as there is no need to recycle mercury


class implementation_is_in_metro_levy_area(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the implementation in a Metropolitan Levy Area as listed in' \
            ' Table A25?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3A (b) (i) - Recognised Energy Saving Activity.'

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


class evidence_obtained_for_refrigerant_disposal(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has evidence been obtained for the disposal of any refrigerants' \
            ' , such as a tax invoice or recycling receipt?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3A (b) (ii) - Recognised Energy Saving Activity.'


class efficiency_of_new_equipment_greater_than_average_equivalent(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the efficiency of energy consumption of the new end user' \
            ' equipment greater than the average efficiency of new equipment' \
            ' that provides the same type, function, output or service?'  # note \
    # that IPART decides which of these three values to use for determining this: \
    # 1. baseline_efficiency_for_end_user_equipment_class \
    # 2. sales_weighted_market_baseline_efficiency \
    # 3. product_weighted_average_baseline_efficiency.
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3B - Recognised Energy Saving Activity.'


class baseline_efficiency_for_end_user_equipment_class(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'As published by the Scheme Administrator, what is the baseline' \
            ' efficiency for this class of End-User Equipment?'  # note that \
    # the concept of "End User Equipment" is not defined in the Rule! \
    # also this should probably directly pull from the Scheme \
    # Administrator's Product Class baseline efficiency list
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' clause 5.3B (a) - Recognised Energy Saving Activity.'


class sales_weighted_market_baseline_efficiency(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'As supported by sales-weighted market data, what is the baseline' \
            ' efficiency for the class of End-User Equipment?'


class product_weighted_average_baseline_efficiency(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'As supported by product-weighted efficiency data, based on' \
            ' products registered as complying with the relevant AS/NZS, what' \
            ' is the baseline efficiency for the class of End-User Equipment?'


class regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'

    def formula(buildings, period, parameters):
        postcode = buildings('postcode', period)
        rnf = parameters(period).energy_savings_scheme.table_a24.regional_network_factor
        return rnf.calc(postcode)   # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided


class activity_meets_all_RESA_criteria(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the activity meet all of the criteria detailed in clause 5.3?'  # note that \
    # the formula below (return where...) is written in that way to reflect \
    # the intention of removal activities being required to meet the addition \
    # criteria detailed in Clause 5.3A, and installation of new equipment needing to
    # meet additional criteria in Clause 5.3B.
    # Essentially, where the activity is \
    # a removal activity, it has to meet Clause 5.3 and Clause 5.3A, where \
    # the activity is NOT a removal activity, it only has to meet Clause 5.3.

    def formula(buildings, period, parameters):
        increased_efficiency = buildings('resa_criteria_increased_efficiency', period)
        reduces_production_or_service_levels = buildings('activity_reduces_production_or_service_levels', period)
        in_jurisdiction = buildings('site_in_ESS_jurisdiction', period)
        activity_is_unlawful = buildings('activity_is_unlawful', period)
        increases_consumption_efficiency = buildings('activity_increases_efficiency_of_energy_consumption', period)
        return (increased_efficiency * (not(reduces_production_or_service_levels))
        * in_jurisdiction * (not(activity_is_unlawful)) * increases_consumption_efficiency)
