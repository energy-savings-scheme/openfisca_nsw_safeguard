import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class F17_equipment_new_installation(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the installation of a new heat pump water heater?',
      'sorting' : 1,
      'eligibility_clause' : """In ESS F17 the activity definition states that the activity must be the installation of one or more air source heat pump water heater systems."""
    }


class F17_4234_certified(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User equipment AS/NZ 4234 certified?',
      'sorting' : 2,
      'eligibility_clause' : """In ESS F17 Equipment Requirements Clause 1 it states that the New End-User Equipment must be an air source heat pump water heater as defined by AS/NZS 4234."""
    }


class F17_installed_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Has installation of the new equipment been performed or supervised by a suitably licensed person?',
      'sorting' : 3,
      'eligibility_clause' : """In ESS F17 Implementation Requirements Clause 2 it states that the activity must be performed or supervised by a suitably qualified licence holder in compliance with the relevant standards and legislation."""
    }
    

class F17_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 4,
        'eligibility_clause' : """In ESS Clause 6.2 it states that an Accredited Certificate Provider may only create Energy Savings Certificates in respect of the Energy Savings for an Implementation where:<br />
                                  (a) the Accredited Certificate Provider is the Energy Saver for those Energy Savings as at the Implementation Date; and <br />
                                  (b) the Accredited Certificate Provider’s Accreditation Date for that Recognised Energy Saving Activity is prior to the Implementation Date."""
    }


class F17_minimum_payment(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Are you aware that you are required to make a minimum payment towards the cost of your upgrade?',
      'sorting' : 5,
      'eligibility_clause' : """In ESS Clause 9.9.1K it states that the Accredited Certificate Provider has evidence satisfactory to the Scheme Administrator that the Purchaser has paid for the Implementation, assessment and other associated works carried out at the Site a Net Amount of at least $200 (excluding GST) for each item of End-User Equipment installed as part of an Implementation using any of Activity Definitions F1.1, F1.2, F16 or F17."""
    }


class F17_building_BCA_not_class_1_or_4(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User Equipment installed in a BCA Class 1 or 4 building?',
      'sorting' : 6,
      'eligibility_clause' : """In ESS F17 Eligibility Requirements Clause 1 it states that the New End-User Equipment must not be installed in a BCA Class 1 or 4 building."""
    }


class F17StorageVolume(Enum):
    less_than_or_equal_to_700_L = 'Less than or equal to 700 litres'
    more_than_700_L = 'More than 700 litres'


class F17_storage_volume(Variable):
    value_type = Enum
    entity = Building
    default_value = F17StorageVolume.more_than_700_L
    possible_values = F17StorageVolume
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'What is the storage volume of the End-User equipment (litres)?',
      'sorting' : 7,
      'eligibility_clause' : """In ESS F17 Equipment Requirements Clause 3 it states that the New End-User Equipment must be certified to comply with AS/NZS 2712 if it has a storage volume less than or equal to 700L"""
    }
    

class F17_storage_volume_int(Variable):
    value_type = int
    entity = Building 
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      storage_volume = buildings('F17_storage_volume', period)

      storage_volume_int = np.select([
          storage_volume == 'Less than or equal to 700 litres',
          storage_volume == 'More than 700 litres'
      ],
      [
        F17StorageVolume.less_than_or_equal_to_700_L,
        F17StorageVolume.more_than_700_L
      ])

      return storage_volume_int


class F17_certified(Variable):
    #only show this if the storage volume is 700L or less 
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User equipment AS/NZ 2712 certified?',
      'sorting' : 8,
      'conditional' : 'True',
      'eligibility_clause' : """In ESS F17 Equipment Requirements Clause 3 it states the installed End-User Equipment must be certified to comply with AS/NZS 2712 if it has a storage volume less than or equal to 700L."""
    }


class F17_equipment_certified_by_storage_volume(Variable):
    """Checks if storage volume is less than or equal to 700L, and if it is, that it is certified by AS/NZS 2712"""
    value_type = bool
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      storage_volume = buildings('F17_storage_volume', period)
      certified_AS_NZ_2712 = buildings('F17_certified', period)

      eligible_by_storage = np.select(
        [
          (storage_volume == F17StorageVolume.less_than_or_equal_to_700_L) * certified_AS_NZ_2712,
          (storage_volume == F17StorageVolume.less_than_or_equal_to_700_L) * np.logical_not(certified_AS_NZ_2712),
          (storage_volume == F17StorageVolume.more_than_700_L)
        ],
        [
          True,
          False,
          True
        ])
      return eligible_by_storage
