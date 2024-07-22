import numpy as np
from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class WH1_F16_electric_PDRSAug24__equipment_replaced(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the activity the replacement of an existing electric hot water boiler or water heater with an (air source) heat pump water heater?',
      'sorting' : 1,
      'eligibility_clause' : """In PDRS WH1 the activity definition states that the activity must replace one or more existing hot water boilers or water heaters with one or more air source heat pump water heater systems."""
    }


class WH1_F16_electric_PDRSAug24__existing_equipment_removed(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the existing End-User equipment been removed?',
        'sorting' : 2,
        'eligibility_clause' : """In PDRS WH1 Implementation Requirements Clause 1 it states that the existing End-User Equipment must be removed."""
    }


class WH1_F16_electric_PDRSAug24__equipment_installed_on_site(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Has the replacement water heater been installed on Site?',
        'sorting' : 3,
        'eligibility_clause' : """In PDRS WH1 Implementation Requirements Clause 2 it states that the replacement End-User Equipment must be installed."""
    }


class WH1_F16_electric_PDRSAug24__qualified_install_removal(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Will the removal of the existing equipment and the installation of the End-User equipment be performed or supervised by a suitably licensed person?',
      'sorting' : 4,
      'eligibility_clause' : """In PDRS WH1 Implementation Requirements Clause 3 it states that the activity, including the removal of any existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class WH1_F16_electric_PDRSAug24__engaged_ACP(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Will an Accredited Certificate Provider be engaged before the implementation date?',
      'sorting' : 5,
      'eligibility_clause' : """In ESS Clause 6.2 it states that an Accredited Certificate Provider may only create Energy Savings Certificates in respect of the Energy Savings for an Implementation where:<br />
                                  (a) the Accredited Certificate Provider is the Energy Saver for those Energy Savings as at the Implementation Date; and <br />
                                  (b) the Accredited Certificate Provider’s Accreditation Date for that Recognised Energy Saving Activity is prior to the Implementation Date."""
    }


class WH1_F16_electric_PDRSAug24__minimum_payment(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {  
      'display_question' : 'Are you aware that you are required to make a minimum payment towards the cost of your upgrade?',
      'sorting' : 6,
      'eligibility_clause' : """In ESS Clause 9.8.1E it states that the Accredited Certificate Provider has evidence satisfactory to the Scheme Administrator that the Purchaser has paid for the Implementation, assessment and other associated works carried out at the Site a Net Amount of at least $200 (excluding GST) for each item of End-User Equipment installed as part of an Implementation using any of Activity Definitions F1.1, F1.2, F16 or F17."""
    }


class WH1_F16_electric_PDRSAug24__building_BCA_not_class_1_or_4(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User Equipment installed in a BCA Class 1 or 4 building?',
      'sorting' : 7,
      'eligibility_clause' : """In PDRS WH1 Eligibility Requirements Clause 3 it states that the End-User Equipment must not be installed in a BCA Class 1 or 4 building."""
    }


class WH1_F16_electric_PDRSAug24__4234_certified(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {  
      'display_question' : 'Is the End-User equipment AS/NZ 4234 certified?',
      'sorting' : 8,
      'eligibility_clause' : """In PDRS WH1 Equipment Requirements Clause 1 it states that The installed End-User Equipment must be an air source heat pump water heater as defined by AS/NZS 4234."""
    }


class WH1_F16_electric_PDRSAug24__scheme_admin_approved(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {  
      'display_question' : 'Has the installed end user equipment been accepted by the Scheme Administrator?',
      'sorting' : 9,
      'eligibility_clause' : """In PDRS WH1 Equipment Requirements Clause 5 it states that the installed End-User Equipment must be accepted in a manner determined by the Scheme Administrator."""
    }


class WH1_F16_electric_PDRSAug24__minimum_annual_energy(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {  
      'display_question' : 'Has the model met the 60% minimum annual energy savings requirement?',
      'sorting' : 10,
      'eligibility_clause' : """In PDRS WH1 Equipment Requirements Clause 2 it states that the installed End-User Equipment must achieve minimum annual energy savings, when determined in accordance with the modelling procedure published by the Scheme Administrator, of:<br />
                                  (a) 60% when modelled in AS/NZS 4234 climate zone HP3-AU if the Site is in BCA Climate Zone 2, 3, 4, 5 or 6; and <br />
                                  (b) 60% when modelled in AS/NZS 4234 climate zone HP5-AU if the Site is in BCA Climate Zone 7 or 8."""
    }

#we want to ask the user if their volume is less than 425 litres, and if it is show them the not eligible for PRCs clauses.


class WH1_F16_electric_PDRSAug24__StorageVolume(Enum):
    less_than_425_L = 'Less than 425 litres'
    equal_425_L_to_700_L = '425 - 700 litres'
    more_than_700_L = 'More than 700 litres'

    
class WH1_F16_electric_PDRSAug24__storage_volume(Variable):
    value_type = Enum
    entity = Building
    default_value = WH1_F16_electric_PDRSAug24__StorageVolume.more_than_700_L
    possible_values = WH1_F16_electric_PDRSAug24__StorageVolume
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'What is the storage volume of the End-User equipment (litres)? (Only storage volume of 425 litres or greater is eligible for PRCs)',
      'sorting' : 11,
    }


class WH1_F16_electric_PDRSAug24__certified(Variable):
    #only show this if the storage volume is 700L or less
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User equipment AS/NZ 2712 certified?',
      'sorting' : 12,
      'conditional' : 'True',
      'eligibility_clause' : """In PDRS WH1 Equipment Requirements Clause 3 it states the installed End-User Equipment must be certified to comply with AS/NZS 2712 if it has a storage volume less than or equal to 700L."""
    }
   

class WH1_F16_electric_PDRSAug24__equipment_certified_by_storage_volume(Variable):
    """Checks if storage volume is less than or equal to 700L, and if it is, that it is certified by AS/NZS 2712
    """
    value_type = bool
    entity = Building
    definition_period = ETERNITY

    def formula(buildings, period, parameters):
      storage_volume = buildings('WH1_F16_electric_PDRSAug24__storage_volume', period)
      certified_AS_NZ_2712 = buildings('WH1_F16_electric_PDRSAug24__certified', period)

      eligible_by_storage = np.select(
        [
          (storage_volume == WH1_F16_electric_PDRSAug24__StorageVolume.less_than_425_L) * certified_AS_NZ_2712,
          (storage_volume == WH1_F16_electric_PDRSAug24__StorageVolume.less_than_425_L) * np.logical_not(certified_AS_NZ_2712),
          (storage_volume == WH1_F16_electric_PDRSAug24__StorageVolume.equal_425_L_to_700_L) * certified_AS_NZ_2712,
          (storage_volume == WH1_F16_electric_PDRSAug24__StorageVolume.equal_425_L_to_700_L) * np.logical_not(certified_AS_NZ_2712),
          (storage_volume == WH1_F16_electric_PDRSAug24__StorageVolume.more_than_700_L)
        ],
        [
          True,
          False,
          True,
          False,
          True
        ])
      return eligible_by_storage
