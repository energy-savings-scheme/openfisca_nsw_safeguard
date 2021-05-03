# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F7_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F6?'

    def formula(buildings, period, parameters):
        rated_output = buildings('F7_rated_output', period)
        business_classification = buildings('business_classification', period)
        BusinessClassification = (business_classification.possible_values)
        end_use_service = buildings('end_use_service', period)
        EndUseService = (end_use_service.possible_values)
        motor_size = select([rated_output >= 0.73 and rated_output < 2.6,
                             rated_output >= 2.6 and rated_output < 9.2,
                             rated_output >= 9.2 and rated_output < 41,
                             rated_output >= 41 and rated_output < 100,
                             rated_output >= 100 and rated_output < 185],
                            ['0_73_to_2_6_kW',
                             '2_6_to_9_2_kW',
                             '9_2_to_41_kW',
                             '41_to_100_kW',
                             '100_to_185_kW'])
        business_classification_is_unknown = (business_classification == BusinessClassification.Unknown)
        end_use_service_is_unknown = (end_use_service == EndUseService.unknown)
        load_utilisation_factor = where((business_classification_is_unknown + end_use_service_is_unknown),
                                        (load_utilisation_factor == parameters(period).HEAB.F7.table_F7_2.default_load_utilisation_factor[motor_size]),
                                        (load_utilisation_factor == parameters(period).HEAB.F7.table_F7_1.default_load_utilisation_factor[business_classification][end_use_service]))
        new_efficiency = buildings('F7_new_product_efficiency', period)
        baseline_efficiency = buildings('F7_baseline_efficiency', period)
        baseline_efficiency = where(baseline_efficiency == 0,
                                    baseline_efficiency == parameters(period).HEAB.F7.table_F7_3.baseline_efficiency[motor_size][frequency][number_of_poles],
                                    baseline_efficiency)
        asset_life = parameters(period).HEAB.F7.table_F7_4.asset_life[motor_size]
        hours_in_year = parameters(period).general_ESS.hours_in_year
        MWh_conversion = parameters(period).general_ESS.unit_conversion_factors['kWh_to_MWh']
        return (rated_output * load_utilisation_factor * ((new_efficiency / baseline_efficiency) / 100)
               * asset_life * hours_in_year / MWh_conversion)
        # note still need to figure out what linear interpolation is and how it impacts on Baseline Efficiency.


class F7_rated_output(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the rated output of the new electric motor, as recorded' \
            ' in the GEMS Registry, in kW?'


class F7_new_product_efficiency(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the full load efficiency of the new electric motor, in %,' \
            ' as recorded in the GEMS Registry?'


class F7_baseline_efficiency(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the full load efficiency of the existing electric motor, in %,' \
            ' as recorded in the GEMS Registry?'
