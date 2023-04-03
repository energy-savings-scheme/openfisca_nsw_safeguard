from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

from openfisca_nsw_safeguard.regulation_reference import PDRS_2022
from openfisca_nsw_safeguard.variables.ESS_general.ESS_BCA_climate_zone import BCA_climate_zone

import numpy as np

class PDRS_WH1_implementation_requirements_existing_hot_water_pump_is_removed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the existing end user equipment been removed?'
    metadata = {
        'alias':  'The existing hot water pump has been removed'
    }

class PDRS_WH1_implementation_requirements_replacement_hot_water_pump_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the replacement End-User equipment been installed?'
    metadata = {
        'alias':  'The replacement hot water pump is installed'
    }

class PDRS_WH1_implementation_requirements_install_or_removal_hot_water_pump_is_installed_by_certified(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the installation and removal of the End-User equipment been performed or supervised by a suitably licensed person?'
    metadata = {
        'alias':  'The installation and removal has been supervised or performed by suitably licensed person' 
    }

class PDRS_WH1_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End-User equipment meet the Implementation Requirements?'
    metadata = {
        'alias':  'The new End-User equipment meets the implementation requirements'
    }

    def formula(buildings, period, parameters):  
        Existing_hot_water_pump_removed = buildings('PDRS_WH1_implementation_requirements_existing_hot_water_pump_is_removed', period)
        Replacement_hot_water_pump_equipment_installed = buildings('PDRS_WH1_implementation_requirements_replacement_hot_water_pump_is_installed', period)
        Installed_or_removed_by_certified = buildings('PDRS_WH1_implementation_requirements_install_or_removal_hot_water_pump_is_installed_by_certified', period)
     
        return (
                Existing_hot_water_pump_removed *
                Replacement_hot_water_pump_equipment_installed *
                Installed_or_removed_by_certified
                )