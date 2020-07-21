# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F1_3_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End User Equipment installed?'
    # no formula for what it means to be installed like F1.1 and F1.2?

class F1_3_installation_is_conducted_by_trades_person(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the installation conducted by a tradesperson?'


class F1_3_installing_tradesperson_has_refrigerant_handling_license(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the tradesperson installing the RDC have a refrigerant' \
            ' handling license?'


class F1_3_installing_tradesperson_has_fair_trading_license(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the tradesperson installing the RDC have a NSW Fair Trading' \
            ' License?'
    # do they need a fair trading license?

class F1_3_tradesperson_has_undertaken_air_conditioning_work_with_refrigeration_class_license(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the tradesperson undertaken air conditioning work with a' \
            ' Refrigeration licence class?'
    # what does this mean? when do they have to have undertaken the work? \
    # is this once? is this before every installation? this is vaguely written.


class F1_3_tradesperson_has_undertaken_refrigeration_work_with_refrigeration_class_license(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the tradesperson undertaken refrigeration work with a' \
            ' Refrigeration licence class?'
    # as above.


class F1_3_electricial_work_is_being_undertaken(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is electricial work being undertaken as part of the installation?'


class F1_3_electricial_work_is_being_undertaken_by_suitably_qualified_person(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is electricial work being undertaken as part of the installation' \
            ' being conducted by a suitably qualified person?'
    # who is suitably qualified?


class F1_3_meets_installation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the Installation meet all of the Installation Requirements?'

    def formula(buildings, period, parameters):
        is_installed = buildings('F1_3_is_installed', period)
        installation_conducted_by_tradesperson = buildings('F1_3_installation_is_conducted_by_trades_person', period)
        tradesperson_has_refrigerant_handling_license = buildings('F1_3_installing_tradesperson_has_refrigerant_handling_license', period)
        tradesperson_has_fair_trading_license = buildings('F1_3_installing_tradesperson_has_fair_trading_license', period)
        tradesperson_has_undertaken_AC_work_with_refrigeration_license = buildings('F1_3_tradesperson_has_undertaken_air_conditioning_work_with_refrigeration_class_license', period)
        tradesperson_has_undertaken_refrigeration_work_with_refrigeration_license = buildings('F1_3_tradesperson_has_undertaken_refrigeration_work_with_refrigeration_class_license', period)
        has_electricial_work = buildings('F1_3_electricial_work_is_being_undertaken', period)
        electrical_work_undertaken_by_qualified_person = buildings('F1_3_electricial_work_is_being_undertaken_by_suitably_qualified_person', period)
        return (is_installed * (installation_conducted_by_tradesperson * tradesperson_has_refrigerant_handling_license)
        * ((tradesperson_has_fair_trading_license * tradesperson_has_undertaken_AC_work_with_refrigeration_license
        + tradesperson_has_undertaken_refrigeration_work_with_refrigeration_license) + (not(tradesperson_has_fair_trading_license)))
        * ((has_electricial_work * electrical_work_undertaken_by_qualified_person) + (not(has_electricial_work))))
