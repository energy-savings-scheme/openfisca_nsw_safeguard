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
      'eligibility_clause' : """In ESS F16 Eligibility Requirements Clause 1 it states that the existing End-User Equipment must be a gas or electric resistance hot water boiler(s) or water heater(s).<br />
                                ESS F16 Eligibility Requirements Clause 3 also states that the existing End-User Equipment must be a gas hot water boiler(s) or gas water heater(s) if the new End-User Equipment is a gas boosted air sourced heat pump."""
    }


class F16_gas_installed_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
        'display_question' : 'Will the removal of the existing equipment and the installation of the End-User equipment be performed or supervised by a suitably licensed person?',
        'sorting' : 2,
        'eligibility_clause' : """In ESS F16 Implementation Requirements Clause 3 it states that the activity, including the removal of any existing End-User Equipment, must be performed or supervised by a suitably Licensed person in compliance with the relevant standards and legislation."""
    }


class F16_gas_split_system(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User equipment a split system?',
      'sorting' : 3,
      'eligibility_clause' : """In ESS D17 Implementation Requirements Clause 4 it states that the where the replacement End-User Equipment is a split system with refrigerant flows between the evaporator and tank, safety requirements of AS/NZS 5149.3:2016 and manufacturer installation recommendations must be followed."""
    }


class F16_gas_safety_requirement(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Have safety requirements of AS/NZS 5149.3:2016 and manufacturer installation recommendations been followed for the installation?',
      'sorting' : 4,
      'eligibility_clause' : """In ESS F16 Implementation Requirements Clause 4 it states that the where the replacement End-User Equipment is a split system with refrigerant flows between the evaporator and tank, safety requirements of AS/NZS 5149.3:2016 and manufacturer installation recommendations must be followed."""
    }


class F16_gas_engaged_ACP(Variable):
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


class F16_gas_minimum_payment(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Are you aware that you are required to make a minimum payment towards the cost of your upgrade?',
      'sorting' : 6,
      'eligibility_clause' : """In ESS Clause 9.9.1E it states that the Accredited Certificate Provider has evidence satisfactory to the Scheme Administrator that the Purchaser has paid for the Implementation, assessment and other associated works carried out at the Site a Net Amount of at least $1000 (excluding GST) for each item of End-User Equipment installed as part of an Implementation using any of Activity Definitions F1.1, F1.2, F16 or F17."""
    }


class F16_gas_building_BCA_not_class_1_or_4(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User Equipment installed in a BCA Class 1 or 4 building?',
      'sorting' : 7,
      'eligibility_clause' : """In ESS F16 Eligibility Requirements Clause 4 it states that the End-User Equipment must not be installed in a BCA Class 1 or 4 building."""
    }


class F16_gas_4234_certified(Variable):
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {  
      'display_question' : 'Is the End-User equipment AS/NZ 4234 certified?',
      'sorting' : 8,
      'eligibility_clause' : """In ESS F16 Equipment Requirements Clause 1 it states that the installed End-User Equipment must be an air source heat pump water heater as defined by AS/NZS 4234"""
    }

    
class F16_gas_storage_volume(Variable):
    value_type = bool
    entity = Building
    default_value = False
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the storage volume of the End-User equipment 700 litres or less?',
      'sorting' : 9,
      'eligibility_clause' : """In ESS F16 gas Equipment Requirements Clause 3 it states the installed End-User Equipment must be certified to comply with AS/NZS 2712 if it has a storage volume less than or equal to 700L."""
    }


class F16_gas_certified(Variable):
    #only show this if the storage volume is 700L or less
    value_type = bool
    entity = Building
    default_value = True
    definition_period = ETERNITY
    metadata = {
      'display_question' : 'Is the End-User equipment AS/NZ 2712 certified?',
      'sorting' : 10,
      'conditional' : 'True',
      'eligibility_clause' : """In ESS F16 Equipment Requirements Clause 3 it states that the installed End-User Equipment must be certified to comply with AS/NZS 2712 if it has a storage volume less than or equal to 700L."""
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
          storage_volume * certified_AS_NZ_2712,
          storage_volume * np.logical_not(certified_AS_NZ_2712),
          np.logical_not(storage_volume) * (certified_AS_NZ_2712),
          np.logical_not(storage_volume) * np.logical_not(certified_AS_NZ_2712)
        ],
        [
          True,
          False,
          True,
          True
        ])
      return eligible_by_storage
