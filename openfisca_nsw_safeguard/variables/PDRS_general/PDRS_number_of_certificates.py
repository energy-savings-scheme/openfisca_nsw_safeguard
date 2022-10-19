from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building
import numpy as np


class PDRS_number_of_peak_demand_reduction_certificates(Variable):
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = 'How many PRCs were created as a result of the peak demand' \
            ' reduction activity?'
    metadata = {
        "variable-type": "inter-interesting",
        "alias": "PDRS Number of Certificates",
    }

    def formula(buildings, period, parameters):
        postcode = buildings('PDRS__postcode', period)
        activity_type = buildings('PDRS_activity_type', period)
        PDRSActivity = activity_type.possible_values
        peak_demand_reduction_capacity = np.select(
                                                    [
                                                        (activity_type == PDRSActivity.replace_motors),
                                                        (activity_type == PDRSActivity.install_motors),
                                                    ],
                                                    [
                                                        buildings('PDRS_HEAB_motors_replace_peak_demand_savings', period),
                                                        buildings('PDRS_HEAB_motors_install_peak_demand_savings', period),
                                                    ]
                                                    )
        regional_network_factor = buildings('PDRS__regional_network_factor', period)
        return np.floor(peak_demand_reduction_capacity * regional_network_factor)
        # check w. Steve/Rod if we round down


class PDRS__postcode(Variable):
    # this variable is used as the first input on all estimator certificate calculation pages
    value_type = int
    entity = Building
    definition_period = ETERNITY
    label = "What is the postcode for the building you are calculating PRCs for?"
    metadata={
        'variable-type' : 'user-input',
        'alias' : 'PDRS Postcode',
        'display_question' : 'What is your postcode?',
        'sorting' : '1'
        }


class PDRSActivity(Enum):
    replace_AC = 'The implementation uses the replace AC activity definition.'
    install_AC = 'The implementation uses the install AC activity definition.'
    replace_motors = 'The implementation uses the Replace Motors activity definition.'
    install_motors = 'The implementation uses the Install Motors activity definition.'
    install_RC = 'The implementation uses the install RC activity definition.'
    remove_fridge = 'The implementation uses the remove fridge activity definition.'
    replace_water_heater = 'The implementation uses the replace water heater activity definition.'


class PDRS_activity_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = PDRSActivity
    default_value = PDRSActivity.replace_AC
    definition_period = ETERNITY
    label = 'What is the activity that is being conducted?'
    metadata={
    "variable-type": "user-input",
    "alias":"PDRS Activity Type",
    # "major-cat":"Peak Demand Reduction Scheme",
    # "monor-cat":'Peak Demand Reduction Scheme - General'
    }

class PDRS__regional_network_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Regional Network Factor is the value from Table A24 of Schedule' \
            ' A corresponding to the postcode of the Address of the Site or' \
            ' Sites where the Implementation(s) took place.'
    metadata={
        "variable-type": "user-input",
        "alias":"PDRS Regional Network Factor",
        # "major-cat":"Peak Demand Reduction Scheme",
        # "monor-cat":'Peak Demand Reduction Scheme - General'
        }

    def formula(buildings, period, parameters):
        postcode = buildings('PDRS__postcode', period)
        rnf = parameters(period).PDRS.table_A24_regional_network_factor
        return rnf.calc(postcode)  # This is a built in OpenFisca function that \
        # is used to calculate a single value for regional network factor based on a zipcode provided
