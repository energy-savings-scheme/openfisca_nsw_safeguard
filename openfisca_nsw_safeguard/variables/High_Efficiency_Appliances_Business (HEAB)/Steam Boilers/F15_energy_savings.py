# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F15_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F15?'

    def formula(buildings, period, parameters):
        current_capacity = buildings('F15_current_equipment_capacity', period)
        operating_pressure = buildings('F15_operating_pressure', period)
        bars_of_pressure = select([operating_pressure < 8,
                                   operating_pressure >= 8 and operating_pressure < 10,
                                   operating_pressure >= 10 and operating_pressure < 12,
                                   operating_pressure >= 12 and operating_pressure < 15,
                                   operating_pressure > 15],
                                  ['eight_bars',
                                   'eight_bars',
                                   'ten_bars',
                                   'twelve_bars',
                                   'fifteen_bars'])
        # note that if less than 8 bars, use 8 bars. if between a tier of bars \
        # (i.e. 9.5 bars) use the lower bar.
        default_efficiency_improvement = parameters(period).HEAB.F15.table_F15_1.default_efficiency_improvement[bars_of_pressure]
        load_utilisation_factor = parameters(period).HEAB.F15.table_F15_2.load_utilisation_factor
        lifetime = parameters(period).HEAB.F15.table_F15_3.lifetime
        hours_in_year = parameters(period).general_ESS.hours_in_year
        MWh_conversion = parameters(period).general_ESS.unit_conversion_factors['kWh_to_MWh']
        return (current_capacity * default_efficiency_improvement * load_utilisation_factor
                * lifetime * hours_in_year / MWh_conversion)


class F15_current_equipment_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the nameplate capacity for the existing equipment, in kW?'


class F15_operating_pressure(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the type of operating pressure of the boiler, as defined' \
            ' in AS3814, in bars of pressure?'
