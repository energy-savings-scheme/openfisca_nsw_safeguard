# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *

import numpy as np


class ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_bars_of_pressure(Variable):
    value_type = str
    entity = Building
    definition_period = ETERNITY
    label = 'What are the bars of pressure for the activity conducted within' \
            ' Activity Definition F14?'

    def formula(buildings, period, parameters):
        operating_pressure = buildings('ESS_HEAB_steam_boiler_new_equipment_operating_pressure', period)
        bars_of_pressure = np.select(
                                [
                                        operating_pressure < 8,
                                        (operating_pressure >= 8) * (operating_pressure < 10),
                                        (operating_pressure >= 10) * (operating_pressure < 12),
                                        (operating_pressure >= 12) * (operating_pressure < 15),
                                        operating_pressure > 15
                                   ],
                                  [
                                        'under_eight_bars',
                                        'eight_bars',
                                        'ten_bars',
                                        'twelve_bars',
                                        'fifteen_bars'
                                   ]
                                   )
        return (bars_of_pressure)


class ESS_HEAB_install_blowdown_flash_heat_recovery_system_on_gas_boiler_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F14?'

    def formula(buildings, period, parameters):
        current_capacity = buildings('ESS_HEAB_steam_boiler_current_equipment_capacity', period)
        operating_pressure = buildings('ESS_HEAB_steam_boiler_new_equipment_operating_pressure', period)
        bars_of_pressure = np.select(
                                [
                                        operating_pressure < 8,
                                        (operating_pressure >= 8) * (operating_pressure < 10),
                                        (operating_pressure >= 10) * (operating_pressure < 12),
                                        (operating_pressure >= 12) * (operating_pressure < 15),
                                        operating_pressure > 15
                                   ],
                                  [
                                        'under_eight_bars',
                                        'eight_bars',
                                        'ten_bars',
                                        'twelve_bars',
                                        'fifteen_bars'
                                    ]
                                    )
        # note that if less than 8 bars, use 8 bars. if between a tier of bars \
        # (i.e. 9.5 bars) use the lower bar.
        default_efficiency_improvement = parameters(period).ESS.HEAB.table_F14_1.default_efficiency_improvement[bars_of_pressure]
        load_utilisation_factor = parameters(period).ESS.HEAB.table_F14_2.load_utilisation_factor
        lifetime = parameters(period).ESS.HEAB.table_F14_3.lifetime
        hours_in_year = parameters(period).ESS.ESS_related_constants.hours_in_year
        return (
                current_capacity * 
                default_efficiency_improvement * 
                load_utilisation_factor * 
                lifetime * 
                hours_in_year / 
                1000
                )