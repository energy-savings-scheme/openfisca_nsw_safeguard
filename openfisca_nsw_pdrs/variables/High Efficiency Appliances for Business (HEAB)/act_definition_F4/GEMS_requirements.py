# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F4_GEMS_MEPS_requirement(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the AC complies with the relevant GEMS MEPS' \
            ' requirements for ACs without variable capacity, as defined' \
            ' in section 21 of the Greenhouse and Energy Minimum Standards' \
            ' (Air Conditioners up to 65kW) Determination 2019'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        MEPS_value = parameters(period).F4.MEPS_values[product_class]
        cooling_capacity = buildings('cooling_capacity', period)
        heating_capacity = buildings('heating_capacity', period)
        return where((cooling_capacity == 0),
                    (heating_capacity > MEPS_value),
                    (cooling_capacity > MEPS_value))


class ACProductClass(Enum):
    product_class_one = 'AC is an air to air unitary air conditioner, which' \
                        ' is wall-mounted, unitary, and double ducted, and' \
                        ' which has a standard cooling full capacity, or' \
                        ' if heating only, a standard heating capacity of' \
                        ' under 65kW.'
    product_class_two = 'AC is an air to air unitary air conditioner, which' \
                        ' is portable, unitary, and double ducted, and' \
                        ' which has a standard cooling full capacity, or' \
                        ' if heating only, a standard heating capacity of' \
                        ' under 65kW.'
    product_class_three = 'AC is an air to air unitary air conditioner, which' \
                          ' is wall mounted, unitary, and single ducted, and' \
                          ' which has a standard cooling full capacity, or' \
                          ' if heating only, a standard heating capacity of' \
                          ' under 65kW.'
    product_class_four = 'AC is an air to air unitary air conditioner, which' \
                         ' is portable, unitary, and single ducted, and' \
                         ' which has a standard cooling full capacity, or' \
                         ' if heating only, a standard heating capacity of' \
                         ' under 10kW.'
    product_class_five = 'AC is an air to air unitary air conditioner, which' \
                         ' is ducted or non-ducted, which is not wall mounted' \
                         ' or portable, and which has a standard cooling full' \
                         ' capacity, or if heating only, a standard heating' \
                         ' capacity of under 10kW.'
    product_class_six = 'AC is an air to air unitary air conditioner, which' \
                        ' is ducted or non-ducted, which is not wall mounted' \
                        ' or portable, and which has a standard cooling full' \
                        ' capacity, or if heating only, a standard heating' \
                        ' capacity of over or equal to 10kW, and under or' \
                        ' equal to 39kW.'
    product_class_seven = 'AC is an air to air unitary air conditioner, which' \
                          ' is ducted or non-ducted, which is not wall mounted' \
                          ' or portable, and which has a standard cooling full' \
                          ' capacity, or if heating only, a standard heating' \
                          ' capacity of over 39kW, and under or equal to 65kW.'
    product_class_eight = 'AC is an air to air single-split air conditioner,' \
                          ' which is non-ducted, and which has a standard' \
                          ' cooling full capacity, or if heating only, a' \
                          ' standard heating capacity of under 4kW.'
    product_class_nine = 'AC is an air to air single-split air conditioner,' \
                         ' which is non-ducted, and which has a standard' \
                         ' cooling full capacity, or if heating only, a' \
                         ' standard heating capacity of over or equal to 4kW,' \
                         ' and under 10kW.'
    product_class_ten = 'AC is an air to air single-split air conditioner,' \
                        ' which is ducted, and which has a standard' \
                        ' cooling full capacity, or if heating only, a' \
                        ' standard heating capacity of under 10kW.'
    product_class_eleven = 'AC is an air to air single-split air conditioner,' \
                           ' which is ducted or non-ducted, and which has a' \
                           ' standard cooling full capacity, or if heating only,' \
                           ' a standard heating capacity of equal or over 10kW,' \
                           ' and under or equal to 39kW.'
    product_class_twelve = 'AC is an air to air single-split air conditioner,' \
                           ' which is ducted or non-ducted, and which has a' \
                           ' standard cooling full capacity, or if heating only,' \
                           ' a standard heating capacity of over 39kW,' \
                           ' and under or equal to 65kW.'
    product_class_thirteen = 'AC is an air to air single-split outdoor air' \
                             ' conditioner which is supplied or offered for supply' \
                             ' to create a non-ducted system, which is not offered' \
                             ' as part of a single-split system and which has a' \
                             ' standard cooling full capacity, or if heating only' \
                             ' a standard heating capacity of under 4kW.'
    product_class_fourteen = 'AC is an air to air single-split outdoor air' \
                             ' conditioner which is supplied or offered for supply' \
                             ' to create a non-ducted system, which is not offered' \
                             ' as part of a single-split system and which has a' \
                             ' standard cooling full capacity, or if heating only' \
                             ' a standard heating capacity of equal or over 4kW.' \
                             ' and under 10kW.'
    product_class_fifteen = 'AC is an air to air single-split outdoor air' \
                            ' conditioner which is supplied or offered for supply' \
                            ' to create a ducted system, which is not offered' \
                            ' as part of a single-split system and which has a' \
                            ' standard cooling full capacity, or if heating only' \
                            ' a standard heating capacity of under 10kW.'
    product_class_sixteen = 'AC is an air to air single-split outdoor air' \
                            ' conditioner which is supplied or offered for supply' \
                            ' to create a ducted or non-ducted system, which is' \
                            ' not offered as part of a single-split system and' \
                            ' which has a standard cooling full capacity, or' \
                            ' if heating only a standard heating capacity of' \
                            ' over or equal to 10kW, and under or equal to 39kW.'
    product_class_seventeen = 'AC is an air to air single-split outdoor air' \
                              ' conditioner which is supplied or offered for supply' \
                              ' to create a ducted or non-ducted system, which is' \
                              ' not offered as part of a single-split system and' \
                              ' which has a standard cooling full capacity, or' \
                              ' if heating only a standard heating capacity of' \
                              ' over 39kW, and under or equal to 65kW.'
    product_class_eighteen = 'AC is an air to air multi-split outdoor air' \
                             ' conditioner which has a standard cooling full' \
                             ' capacity, or if heating only, a standard heating' \
                             ' capacity of under 4kW.'
    product_class_nineteen = 'AC is an air to air multi-split outdoor air' \
                             ' conditioner which has a standard cooling full' \
                             ' capacity, or if heating only, a standard heating' \
                             ' capacity of over or equal to 4kW, and under 10kW.'
    product_class_twenty = 'AC is an air to air multi-split outdoor air' \
                           ' conditioner which has a standard cooling full' \
                           ' capacity, or if heating only, a standard heating' \
                           ' capacity of over or equal to 10kW, and under 39kW.'
    product_class_twenty_one = 'AC is an air to air multi-split outdoor air' \
                               ' conditioner which has a standard cooling full' \
                               ' capacity, or if heating only, a standard heating' \
                               ' capacity of over or equal to 39kW, and under or' \
                               ' equal to 65kW.'
    product_class_twenty_two = 'AC is an water to air air conditioner which' \
                               ' has a standard cooling full capacity, or if heating' \
                               ' only, a standard heating capacity of under 39kW.'
    product_class_twenty_three = 'AC is an water to air air conditioner which' \
                                 ' has a standard cooling full capacity, or if heating' \
                                 ' only, a standard heating capacity of over or' \
                                 ' equal to 39kW, and under or equal to 65kW.'


class product_class(Variable):
    value_type = Enum
    possible_values = ACProductClass
    default_value = ACProductClass.product_class_one
    entity = Building
    definition_period = ETERNITY
    label = 'returns the product class from the defined list of products in' \
            ' Enum ACProductClass.'
