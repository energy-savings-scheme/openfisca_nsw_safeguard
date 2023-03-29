import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class WH1_equipment_replaced(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the replacement of an existing resistance hot water boiler or heater with a heat pump water heater?',
      'sorting' : 1,
      'eligibility_clause' : """In PDRS WH1 the activity definition states that the activity must replace one or more existing hot water boilers or water heaters with one or more air source heat pump water heater systems."""
    }


class WH1_installation(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the installation of a new heat pump water heater?',
      'sorting' : 2,
      'conditional' : 'True',
      'eligibility_clause' : """This activity is not eligible for PRCs (only eligible for ESCs), in PDRS WH1 the activity definition states that the activity must replace one or more existing hot water boilers or water heaters with one or more air source heat pump water heater systems."""
    }


class WH1_equipment_replaces_electric(Variable):
    #replacement of an existing gas hot water heater or boiler is only eligible for ESCs (not PRCs)
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the equipment being replaced an electric hot water boiler or water heater?',
      'sorting' : 3,
      'eligibility_clause' : """The replacement of a gas hot water heater or boiler is only eligible for ESCs, in PDRS WH1 Eligibility Requirements Clause 1 it states the existing End-User Equipment must be an electric resistance hot water boiler(s) or water heater(s)."""
    }


class WH1_equipment_removed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Has the removal of the existing equipment and the installation of the end-user equipment been performed or supervised by a suitably licensed person?'
    metadata = {
        'display_question' : 'Has the removal of the existing equipment and the installation of the end-user equipment been performed or supervised by a suitably licensed person?',
        'sorting' : 4,
        'eligibility_clause' : """In PDRS WH1 Implementation Requirements Clause 3 it states that the activity, including the removal of any existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class WH1_equipment_installed_and_operational(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Is the new End-User equipment installed and operational?',
        'sorting' : 5,
        'eligibility_clause' : """In PDRS WH1 Implementation Requirements Clause 2 it states that the replacement End-User Equipment must be installed."""
    }


class WH1_building_BCA_not_class_1_or_4(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User Equipment installed in a BCA Class 1 or 4 building?',
      'sorting' : 6,
      'eligibility_clause' : """In PDRS WH1 Eligibility Requirements Clause 3 it states that the End-User Equipment must not be installed in a BCA Class 1 or 4 building."""
    }


class WH1_air_source_heat_pump(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = { 
      'display_question' : 'Is the installed end-user equipment an air source heat pump water heater as defined by AS/NZS 4234?',
      'sorting' : 7,
      'eligibility_clause' : """In PDRS WH1 Equipment Requirements Clause 1 it states that the installed End-User Equipment must be an air source heat pump water heater as defined by AS/NZS 4234."""
    }


class WH1_scheme_admin_approved(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {  
      'display_question' : 'Has the installed end user equipment been accepted by the Scheme Administrator?',
      'sorting' : 8,
      'eligibility_clause' : """In PDRS WH1 Equipment Requirements Clause 4 it states that the installed End-User Equipment must be accepted in a manner determined by the Scheme Administrator."""
    }


class WH1_minimum_savings(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {  
      'display_question' : 'Has the model met the 60% minimum annual energy savings requirement?',
      'sorting' : 9,
      'eligibility_clause' : """In PDRS WH1 Equipment Requirements Clause 2 it states that the installed End-User Equipment must achieve minimum annual energy savings, when determined in accordance with the modelling procedure published by the Scheme Administrator, of: <br />
      a. 60% when modelled in climate zone HP3-AU if the Site is in BCA Climate Zone 2, 3, 4, 5 or 6; <br />
      b. 60% when modelled in climate zone HP5-AU if the Site is in BCA Climate Zone 7 or 8."""
    }


class WH1StorageVolume(Enum):
    less_than_or_equal_to_700_L = 'Less than or equal to 700 litres'
    more_than_700_L = 'More than 700 litres'

    
class WH1_storage_volume(Variable):
    value_type = Enum
    entity = Building
    default_value = WH1StorageVolume.more_than_700_L
    possible_values = WH1StorageVolume
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'What is the storage volume of the End-User equipment (litres)?',
      'sorting' : 10,
      'eligibility_clause' : """In PDRS WH1 Equipment Requirements Clause 3 it states the installed End-User Equipment must be certified to comply with AS/NZS 2712 if it has a storage volume less than or equal to 700L."""
    }


class WH1_storage_volume_int(Variable):
    value_type = int
    entity = Building 
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      storage_volume = buildings('WH1_storage_volume', period)

      storage_volume_int = np.select([
          storage_volume == 'Less than or equal to 700 litres',
          storage_volume == 'More than 700 litres'
      ],
      [
        WH1StorageVolume.less_than_or_equal_to_700_L,
        WH1StorageVolume.more_than_700_L
      ])

      return storage_volume_int


class WH1_certified(Variable):
    #only show this if the storage volume is 700L or less
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User equipment AS/NZ 2712 certified?',
      'sorting' : 11,
      'conditional' : 'True',
      'eligibility_clause' : """In PDRS WH1 Equipment Requirements Clause 3 it states the installed End-User Equipment must be certified to comply with AS/NZS 2712 if it has a storage volume less than or equal to 700L."""
    }
   

class WH1_equipment_certified_by_storage_volume(Variable):
    """Checks if storage volume is less than or equal to 700L, and if it is, that it is certified by AS/NZS 2712
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      storage_volume = buildings('WH1_storage_volume', period)
      certified_AS_NZ_2712 = buildings('WH1_certified', period)

      eligible_by_storage = np.select(
        [
          (storage_volume == WH1StorageVolume.less_than_or_equal_to_700_L) * certified_AS_NZ_2712,
          (storage_volume == WH1StorageVolume.less_than_or_equal_to_700_L) * np.logical_not(certified_AS_NZ_2712),
          (storage_volume == WH1StorageVolume.more_than_700_L)
        ],
        [
          True,
          False,
          True
        ])
      return eligible_by_storage