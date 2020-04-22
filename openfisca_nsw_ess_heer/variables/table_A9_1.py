# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class EquipmentClassStatus(Enum):
    T12_linear = 'A double-capped fluorescent Lamp as defined by AS/NZS' \
                 ' 4782.1 Double-capped fluorescent lamps – Performance' \
                 ' specifications with a tube diameter of 38.1mm. These are' \
                 ' also referred to as T38.'
    T8_linear = 'A double-capped fluorescent Lamp as defined by AS/NZS 4782.1' \
                ' Double-capped fluorescent lamps – Performance specifications'\
                ' with a tube diameter of 25.4mm. These are also referred to' \
                ' as T26.'
    T5_linear = u'A double-capped fluorescent Lamp as defined by AS/NZS 4782.1' \
                ' Double-capped fluorescent lamps – Performance specifications' \
                ' with a tube diameter of 15.9mm.  These are also referred to' \
                ' as T16.'
    T5_or_T8_circular = u'A double-capped circular fluorescent Lamp with a' \
                        ' typical tube diameter of 16mm or 29mm as defined by' \
                        ' AS/NZS 4782.1 Double-capped fluorescent lamps – ' \
                        ' Performance specifications.  These are also referred' \
                        ' to as T9.'
    CFLn = 'An externally ballasted single-capped fluorescent Lamp as defined' \
           ' by AS/NZS 60901 Single-capped fluorescent lamps-Performance' \
           ' specifications.  The Lamp may include an internal means of' \
           ' starting and pre-heated cathodes.'
    CFLi = 'A Self-ballasted compact fluorescent Lamp as defined by AS/NZS' \
           ' 4847 Self-ballasted lamps for general lighting services.'
    tungsten_halogen_240V = u'A Tungsten halogen Lamp as defined in AS 4934' \
                            ' Incandescent lamps for general lighting service,' \
                            ' with a rated voltage of 240V.'
    tungsten_halogen_ELV = 'A Tungsten halogen Lamp as defined in AS 4934' \
                           ' Incandescent lamps for general lighting service,' \
                           ' with an ELV rating, typically 12V.  These Lamps' \
                           ' run off an Extra-low voltage lighting converter' \
                           ' (ELC) as defined in AS 4879.1.'
    infrared_coated_ELV = 'An ELV Tungsten halogen Lamp as defined in AS' \
                          ' 4934 where the halogen globe is coated with a' \
                          ' reflective infrared coating which improves the' \
                          ' efficiency of the globe.'
    metal_halide_lamp = u'A discharge Lamp classified as a Metal halide Lamp as' \
                        ' defined by IEC 61167 Metal halide lamps – Performance' \
                        ' specification.'
    mercury_vapour_lamp = u'A discharge Lamp classified as a High pressure' \
                          ' mercury vapour Lamp as defined by IEC 60188' \
                          ' High-pressure mercury vapour lamps – Performance' \
                          ' specifications.'
    HPS_lamp = 'A discharge Lamp classified as a High pressure sodium vapour' \
               ' Lamp as defined by IEC 60662 High-pressure sodium vapour lamps.'
    lighting_for_roads_and_public_spaces_or_traffic_signals = 'Lighting for' \
                                                              ' Roads and Public' \
                                                              ' spaces as defined' \
                                                              ' by AS 1158 Lighting' \
                                                              ' for roads and' \
                                                              ' public spaces.'
    T5_adaptor_kit = 'Any equipment that enables a T8 or T12 Luminaire to' \
                     ' accommodate or provide physical support to a T5 Lamp' \
                     ' or Luminaire.'
    retrofit_luminaire_LED_linear_lamp = 'A T5, T8 or T12 Luminaire that has' \
                                         ' been retrofitted with an LED linear' \
                                         ' Lamp in place of the linear fluorescent' \
                                         ' Lamp.  This cannot involve modification' \
                                         ' to the wiring of the Luminaire other' \
                                         ' than removal, replacement or' \
                                         ' modification of the starter.'
    LED_lamp_only_ELV = 'An LED Lamp that runs off an existing Extra-low' \
                        ' voltage lighting converter (ELC) designed for' \
                        ' retrofitting into an existing Luminaire or Lamp' \
                        ' holder.  These are typically used as a replacement' \
                        ' for ELV Tungsten halogen Lamps.'
    LED_lamp_only_240V_self_ballasted = u'A self-ballasted LED Lamp as defined' \
                                        ' by AS/NZS 62560 Self-ballasted LED' \
                                        ' lamps for general lighting services' \
                                        ' by voltage > 50 V.  These Lamps are' \
                                        ' connected directly to a 240V supply.'
    induction_luminaire = u'A gas discharge Lamp in which the power required' \
                          ' to generate light is transferred from outside the' \
                          ' Lamp envelope to the gas via electromagnetic' \
                          ' induction.'
    LED_lamp_and_driver = 'A LED-reflector Lamp and matching LED Driver' \
                          ' intended as an alternative to a Mirrored' \
                          ' Reflector Halogen Lamp.'
    modified_luminaire_LED_linear_lamp = 'A T5, T8 or T12 luminaire that has' \
                                         ' been modified for use with an LED' \
                                         ' linear Lamp.  This involves' \
                                         ' modifying, removing or rendering' \
                                         ' redundant any wiring or structure of' \
                                         ' the Luminaire, beyond the' \
                                         ' replacement of a starter.'
    LED_luminaire_fixed_type = 'An LED Luminaire intended for use as a fixed' \
                               ' luminaire as defined in AS/NZS 60598.2.1' \
                               ' Luminaires – Particular requirements – ' \
                               ' Fixed general purpose luminaires.'
    LED_luminaire_linear_lamp = u'An LED Luminaire intended for use as an' \
                                ' alternative to a linear fluorescent' \
                                ' Luminaire, where the Luminaire houses a' \
                                ' matching Linear LED tube or a linear array' \
                                ' of integrated LEDs.  Where the Luminaire' \
                                ' uses a Linear LED tube, the Luminaire must' \
                                ' not be compatible with a linear fluorescent Lamp.'
    LED_luminaire_floodlight = u'An LED Luminaire intended for use as a' \
                               ' floodlight as defined in AS/NZS 60598.2.5' \
                               ' Luminaires – Particular requirements –' \
                               ' Floodlights.'
    LED_luminaire_recessed = u'An LED Luminaire intended for use as a recessed' \
                             ' luminaire as defined in AS/NZS 60598.2.2' \
                             ' Luminaires – Particular requirements –' \
                             ' Recessed luminaires.'
    LED_luminaire_high_low_bay = u'An LED Luminaire intended for use as' \
                                 ' high-bay or low-bay lighting.'
    LED_luminaire_streetlight = u'An LED Luminaire intended for use as a' \
                                ' streetlight as defined in AS/NZS 60598.2.3' \
                                ' Particular requirements – Luminaires for' \
                                ' road and street lighting.'
    LED_luminaire_emergency_lighting = u'An LED Luminaire intended for use as' \
                                       ' an Emergency lighting luminaire as' \
                                       ' defined in AS/NZS 60598.2.22' \
                                       ' Particular requirements – Luminaires' \
                                       ' for emergency lighting.'
    LED_hospital_use = u'An LED Luminaire intended for use in the clinical' \
                       ' areas of a hospital or health care building as' \
                       ' defined in AS/NZS 60958.2.25 Particular requirements' \
                       ' – Luminaires for use in clinical areas of hospitals' \
                       ' and health care buildings.'
    other_emerging_lighting_technology = u'Any lighting equipment not defined' \
                                         ' above.'


class existing_lamp_type(Variable):
    value_type = Enum
    possible_values = EquipmentClassStatus
    default_value = EquipmentClassStatus.T12_linear
    entity = Building
    definition_period = ETERNITY
    label = 'Defines the existing lamp type, as defined in Table A9.1 or Table A9.3' \
            ' in Schedule A.'


class new_lamp_type(Variable):
    value_type = Enum
    possible_values = EquipmentClassStatus
    default_value = EquipmentClassStatus.T12_linear
    entity = Building
    definition_period = ETERNITY
    label = 'Defines the new lamp type, as defined in Table A9.1 or Table A9.3' \
            ' in Schedule A.'
