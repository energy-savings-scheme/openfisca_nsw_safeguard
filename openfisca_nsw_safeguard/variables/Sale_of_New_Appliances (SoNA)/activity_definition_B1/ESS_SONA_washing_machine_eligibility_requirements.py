from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS__SONA_end_user_equipment_is_clothes_washing_machine(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a Clothes Washing Machine?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 1.'


    def formula(buildings, period, parameters):
        equipment_type = buildings('ESS__SONA_equipment_type', period)
        possible_equipment_type = equipment_type.possible_values
        is_washing_machine = (equipment_type == possible_equipment_type.washing_machine)
        return is_washing_machine


class ESS__SONA_equipment_is_top_or_front_loader(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the new End User Equipment a top loader or a front loader?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 3.'
                # change to enum when you get chance


class ESS__SONA_washing_machine_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the washing machine eligible to create energy savings?'
    reference = 'Energy Savings Scheme Rule of 2009, Effective 30 March 2020,' \
                ' Schedule B, Activity Definition B1, Equipment Requirement 3.'
                # change to enum when you get chance

    def formula(buildings, period, parameters):
        is_washing_machine = buildings('ESS__SONA_end_user_equipment_is_clothes_washing_machine', period)
        is_top_or_front_loader = buildings('ESS__SONA_equipment_is_top_or_front_loader', period)
        labelled_for_energy_labelling = buildings('ESS__SONA_equipment_labelled_for_energy_labelling', period)
        return (is_washing_machine * is_top_or_front_loader * labelled_for_energy_labelling)
