import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class F16_gas_equipment_replaced(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the replacement of a gas hot water boiler or heater with a heat pump water heater?',
      'sorting' : 1,
      'eligibility_clause' : """In ESS F16 Eligibility Requirements Clause 1 it states that the existing End-User Equipment must be a gas or electric resistance hot water boiler(s) or water heater(s)."""
    }

# class F16_gas_installation(Variable):
#     value_type = bool
#     entity = Building
#     default_value = True
#     definition_period = ETERNITY
#     metadata = {
#       'display_question' : 'Is the activity the installation of a new heat pump water heater?',
#       'sorting' : 2,
#       'conditional' : 'True',
#       'eligibility_clause' : """This activity is not eligible for PRCs (only eligible for ESCs), in PDRS F16_gas the activity definition states that the activity must replace one or more existing hot water boilers or water heaters with one or more air source heat pump water heater systems."""
#     }


# class F16_gas_equipment_replaces_electric(Variable):
#     value_type = bool
#     entity = Building
#     default_value = True
#     definition_period = ETERNITY
#     metadata = {
#       'display_question' : 'Is the equipment being replaced an electric hot water boiler or water heater?',
#       'sorting' : 3,
#       'eligibility_clause' : """The replacement of a gas hot water heater or boiler is only eligible for ESCs, in PDRS F16_gas Eligibility Requirements Clause 1 it states the existing End-User Equipment must be an electric resistance hot water boiler(s) or water heater(s)."""
#     }


class F16_gas_equipment_removed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    label = 'Will the removal of the existing equipment and the installation of the End-User equipment be performed or supervised by a suitably licensed person?'
    metadata = {
        'display_question' : 'Will the removal of the existing equipment and the installation of the End-User equipment be performed or supervised by a suitably licensed person?',
        'sorting' : 2,
        'eligibility_clause' : """In ESS F16 Implementation Requirements Clause 3 it states that the activity, including the removal of any existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class F16_gas_engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will an Accredited Certificate Provider be engaged before the implementation date?',
        'sorting' : 3,
        'eligibility_clause' : """In ESS Clause 6.2 it states that an Accredited Certificate Provider may only create Energy Savings Certificates in respect of the Energy Savings for an Implementation where:<br />
                                  (a) the Accredited Certificate Provider is the Energy Saver for those Energy Savings as at the Implementation Date; and <br />
                                  (b) the Accredited Certificate Provider’s Accreditation Date for that Recognised Energy Saving Activity is prior to the Implementation Date."""
    }


class F16_gas_building_BCA_not_class_1_or_4(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User Equipment installed in a BCA Class 1 or 4 building?',
      'sorting' : 4,
      'eligibility_clause' : """In ESS F16 Eligibility Requirements Clause 4 it states that the End-User Equipment must not be installed in a BCA Class 1 or 4 building."""
    }


class F16_gas_scheme_admin_approved(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {  
      'display_question' : 'Has the installed end user equipment been accepted by the Scheme Administrator?',
      'sorting' : 5,
      'eligibility_clause' : """In PDRS F16_gas Equipment Requirements Clause 4 it states that the installed End-User Equipment must be accepted in a manner determined by the Scheme Administrator."""
    }


class F16_gasStorageVolume(Enum):
    less_than_or_equal_to_700_L = 'Less than or equal to 700 litres'
    more_than_700_L = 'More than 700 litres'

    
class F16_gas_storage_volume(Variable):
    value_type = Enum
    entity = Building
    default_value = F16_gasStorageVolume.more_than_700_L
    possible_values = F16_gasStorageVolume
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'What is the storage volume of the End-User equipment (litres)?',
      'sorting' : 8,
      'eligibility_clause' : """In PDRS F16_gas Equipment Requirements Clause 3 it states the installed End-User Equipment must be certified to comply with AS/NZS 2712 if it has a storage volume less than or equal to 700L."""
    }


class F16_gas_storage_volume_int(Variable):
    value_type = int
    entity = Building 
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      storage_volume = buildings('F16_gas_storage_volume', period)

      storage_volume_int = np.select([
          storage_volume == 'Less than or equal to 700 litres',
          storage_volume == 'More than 700 litres'
      ],
      [
        F16_gasStorageVolume.less_than_or_equal_to_700_L,
        F16_gasStorageVolume.more_than_700_L
      ])

      return storage_volume_int


class F16_gas_certified(Variable):
    #only show this if the storage volume is 700L or less
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User equipment AS/NZ 2712 certified?',
      'sorting' : 9,
      'conditional' : 'True',
      'eligibility_clause' : """In PDRS F16_gas Equipment Requirements Clause 3 it states the installed End-User Equipment must be certified to comply with AS/NZS 2712 if it has a storage volume less than or equal to 700L."""
    }
   

class F16_gas_equipment_certified_by_storage_volume(Variable):
    """Checks if storage volume is less than or equal to 700L, and if it is, that it is certified by AS/NZS 2712
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      storage_volume = buildings('F16_gas_storage_volume', period)
      certified_AS_NZ_2712 = buildings('F16_gas_certified', period)

      eligible_by_storage = np.select(
        [
          (storage_volume == F16_gasStorageVolume.less_than_or_equal_to_700_L) * certified_AS_NZ_2712,
          (storage_volume == F16_gasStorageVolume.less_than_or_equal_to_700_L) * np.logical_not(certified_AS_NZ_2712),
          (storage_volume == F16_gasStorageVolume.more_than_700_L)
        ],
        [
          True,
          False,
          True
        ])
      return eligible_by_storage