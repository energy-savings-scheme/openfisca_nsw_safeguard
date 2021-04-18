from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS__regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'
    metadata={
        "variable-type": "user-input",
        "alias":"ESS Regional Network Factor",
        "major-cat":"Energy Savings Scheme",
        "monor-cat":'Energy Savings Scheme - General'
        }

    def formula(buildings, period, parameters):
        postcode = buildings('ESS__postcode', period)
        rnf = parameters(period).ESS.ESS_general.table_A24_regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided
