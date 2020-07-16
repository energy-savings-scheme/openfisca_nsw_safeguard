# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class new_lamp_circuit_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Allows the user to input the Lamp Circuit Power for the new lamp' \
            'in W, as measured in accordance with Table A9.4.'
    #  need to put in what activities this is relevant for


class existing_lamp_LCP(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Allows the user to input the Lamp Circuit Power for the new lamp' \
            'in W, as measured in accordance with Table A9.4.'
    #  need to put in what activities this is relevant for


class new_lamp_light_output(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Allows the user to input the light output for the new lamp' \
            'in lm, as measured in accordance with Table A9.4.'
    #  need to put in what activities this is relevant for


class existing_lamp_light_output(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Allows the user to input the light output for the existing lamp' \
            'in lm, as measured in accordance with Table A9.4.'
    #  need to put in what activities this is relevant for


class BCAClimateZone(Enum):
    BCA_Climate_Zones_2_and_3 = 'Implementation takes place in BCA Climate' \
                                ' Zone 2 or BCA Climate Zone 3.'
    BCA_Climate_Zone_4 = 'Implementation takes place in BCA Climate Zone 4.'
    BCA_Climate_Zone_5 = 'Implementation takes place in BCA Climate Zone 5.'
    BCA_Climate_Zone_6 = 'Implementation takes place in BCA Climate Zone 6.'
    BCA_Climate_Zones_7_and_8 = 'Implementation takes place in BCA Climate' \
                                ' Zone 7 or BCA Climate Zone 8.'
    #  need to put in what activities this is relevant for


class BCA_Climate_Zone(Variable):
    value_type = Enum
    possible_values = BCAClimateZone
    default_value = BCAClimateZone.BCA_Climate_Zones_2_and_3
    entity = Building
    definition_period = ETERNITY
    label = 'Defines what Climate Zone, as defined by the BCA, the' \
            ' Implementation is conducted within.'
    #  need to put in what activities this is relevant for


class BuildingType(Enum):
    residential_building = 'Implementation takes place on a Residential' \
                           ' Building, which means a building or part of a' \
                           ' building classified as a BCA Class 1, 2 or 4' \
                           ' building, and may include any Non-Habitable' \
                           ' Building on the same site.'
    small_business_site = 'Implementation takes place on a Small Business' \
                          ' Site, which is defined as a Site that (a) is' \
                          ' entirely occupied by one business; and (b) where' \
                          ' the business, as a consumer of electricity at' \
                          ' the Site: i. is a Small Customer (and, for the' \
                          ' avoidance of doubt, has not aggregated its load' \
                          ' at the Site with consumption at other Sites for' \
                          ' the purposes of being treated as a Large' \
                          ' Customer under its electricity purchase' \
                          ' arrangements); or ii.	is a customer of an Exempt' \
                          ' Seller, and has an annual electricity consumption' \
                          ' below the Upper Consumption Threshold for' \
                          ' electricity.'
    #  need to put in what activities this is relevant for


class building_type(Variable):
    value_type = Enum
    possible_values = BuildingType
    default_value = BuildingType.residential_building
    entity = Building
    definition_period = ETERNITY
    label = 'Defines what building type the Implementation is conducted within.'
    #  need to put in what activities this is relevant for


class ImplementationState(Enum):
    ACT = u"Implementation is in ACT."
    NSW = u"Implementation is in NSW."
    NT = u"Implementation is in NT."
    QLD = u"Implementation is in QLD."
    SA = u"Implementation is in SA."
    TAS = u"Implementation is in TAS."
    VIC = u"Implementation is in VIC."
    WA = u"Implementation is in WA."
    #  need to put in what activities this is relevant for


class implementation_state(Variable):
    value_type = Enum
    entity = Building
    possible_values = ImplementationState
    default_value = ImplementationState.NSW
    definition_period = ETERNITY
    label = "State within which the relevant NABERS rated building is located."
    #  need to put in what activities this is relevant for


class RefrigeratorGroup(Enum):
    group_1 = u"Refrigerator is in Group 1."
    group_2 = u"Refrigerator is in Group 2."
    group_3 = u"Refrigerator is in Group 3."
    group_4 = u"Refrigerator is in Group 4."
    group_5B = u"Refrigerator is in Group 5B."
    group_5S = u"Refrigerator is in Group 5S."
    group_5T = u"Refrigerator is in Group 5T."
    group_6C = u"Refrigerator is in Group 6C."
    group_6U = u"Refrigerator is in Group 6U."
    group_7 = u"Refrigerator is in Group 7."
    #  need to put in what activities this is relevant for


class refrigerator_or_freezer_group(Variable):
    value_type = Enum
    entity = Building
    possible_values = RefrigeratorGroup
    default_value = RefrigeratorGroup.group_1
    definition_period = ETERNITY
    label = "What is the refrigerator group for the new End User Equipment?"
    #  need to put in what activities this is relevant for


class refrigerator_or_freezer_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the capacity of the refrigerator or freezer, in L?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule C, Activity Definition C1, Equipment Requirement 3.'
    #  need to put in what activities this is relevant for


class washing_machine_star_rating(Variable):
    value_type = float  # note need to recode as Enum once reading AS2040
    entity = Building
    definition_period = ETERNITY
    label = 'What is the star rating for the clothes washing machine, as' \
            ' rated in GEMS?'
    #  need to put in what activities this is relevant for


class dryer_star_rating(Variable):
    value_type = float  # note need to recode as Enum once reading AS2040
    entity = Building
    definition_period = ETERNITY
    label = 'What is the star rating for the clothes washing machine, as' \
            ' rated in GEMS?'
    # for use in Activity Definition B3.


class dishwasher_star_rating(Variable):
    value_type = float  # note need to recode as Enum once reading AS2040
    entity = Building
    definition_period = ETERNITY
    label = 'What is the star rating for the dishwasher, as' \
            ' rated in GEMS?'
    # for use in Activity Definition B3.


class number_of_refrigerator_doors(Variable):
    value_type = int  # note need to recode as Enum once reading AS2040
    entity = Building
    definition_period = ETERNITY
    label = 'How many doors does the refrigerator have?'
    # for use in Activity Definition B4, B5.


class refrigerator_star_rating(Variable):
    value_type = float  # note need to recode as Enum once reading AS2040
    entity = Building
    definition_period = ETERNITY
    label = 'What is the star rating for the refrigerator, as' \
            ' rated in GEMS?'
    # for use in Activity Definition B4, B5, B6.


class television_screen_size(Variable):
    value_type = float  # note need to recode as Enum once reading AS2040
    entity = Building
    definition_period = ETERNITY
    label = 'What is the screen size for the television, as' \
            ' rated in GEMS?'
    # for use in Activity Definition B7.


class television_star_rating(Variable):
    value_type = float  # note need to recode as Enum once reading AS2040
    entity = Building
    definition_period = ETERNITY
    label = 'What is the star rating for the television, as' \
            ' rated in GEMS?'
    # for use in Activity Definition B7.


class D1_system_U_value(Variable):
    value_type = float  # note need to recode as Enum once reading AS2040
    entity = Building
    definition_period = ETERNITY
    label = 'What is the system U-Value for the thermally efficient window' \
            ' or door?'
    # for use in Activity Definition D1.


class D2_system_U_value(Variable):
    value_type = float  # note need to recode as Enum once reading AS2040
    entity = Building
    definition_period = ETERNITY
    label = 'What is the system U-Value for the thermally efficient window' \
            ' or door?'
    # for use in Activity Definition D2.


class AS3823CoolingStarRating(Enum):
    no_rating = u'Equipment has no star rating.'
    one_star = u'Equipment has a Star Rating of 1 star, as defined in AS3823.2.'
    one_and_a_half_stars = u'Equipment has a Star Rating of 1.5 stars, as defined in AS3823.2.'
    two_stars = u'Equipment has a Star Rating of 2 stars, as defined in AS3823.2.'
    two_and_a_half_stars = u'Equipment has a Star Rating of 2.5 stars, as defined in AS3823.2.'
    three_stars = u'Equipment has a Star Rating of 3 stars, as defined in AS3823.2.'
    three_and_a_half_stars = u'Equipment has a Star Rating of 3.5 stars, as defined in AS3823.2.'
    four_stars = u'Equipment has a Star Rating of 4 stars, as defined in AS3823.2.'
    four_and_a_half_stars = u'Equipment has a Star Rating of 4.5 stars, as defined in AS3823.2.'
    five_stars = u'Equipment has a Star Rating of 5 stars, as defined in AS3823.2.'
    five_and_a_half_stars = u'Equipment has a Star Rating of 5.5 stars, as defined in AS3823.2.'
    six_stars = u'Equipment has a Star Rating of 6 stars, as defined in AS3823.2.'
    seven_stars = u'Equipment has a Star Rating of 7 stars, as defined in AS3823.2.'
    eight_stars = u'Equipment has a Star Rating of 8 stars, as defined in AS3823.2.'
    nine_stars = u'Equipment has a Star Rating of 9 stars, as defined in AS3823.2.'
    ten_stars = u'Equipment has a Star Rating of 10 stars, as defined in AS3823.2.'


class air_con_cooling_rating(Variable):
    value_type = Enum
    entity = Building
    possible_values = AS3823CoolingStarRating
    default_value = AS3823CoolingStarRating.no_rating
    definition_period = ETERNITY
    label = 'What is the cooling star rating for the air conditioner, as defined in AS3823.2?'


class F1ProductClass(Enum):
    product_class_one = 'RDC is in product class 1.'
    product_class_two = 'RDC is in product class 2.'
    product_class_three = 'RDC is in product class 3.'
    product_class_four = 'RDC is in product class 4.'
    product_class_five = 'RDC is in product class 5.'
    product_class_six = 'RDC is in product class 6.'
    product_class_seven = 'RDC is in product class 7.'
    product_class_eight = 'RDC is in product class 8.'
    product_class_nine = 'RDC is in product class 9.'
    product_class_ten = 'RDC is in product class 10.'
    product_class_eleven = 'RDC is in product class 11.'
    product_class_twelve = 'RDC is in product class 12.'
    product_class_thirteen = 'RDC is in product class 13.'
    product_class_fourteen = 'RDC is in product class 14.'
    product_class_fifteen = 'RDC is in product class 15.'


class F1_product_class(Variable):
    value_type = Enum
    entity = Building
    possible_values = F1ProductClass
    default_value = F1ProductClass.product_class_one
    definition_period = ETERNITY
    label = 'What is the product class for the RDC installed in Activity' \
            ' Definition F1?'
