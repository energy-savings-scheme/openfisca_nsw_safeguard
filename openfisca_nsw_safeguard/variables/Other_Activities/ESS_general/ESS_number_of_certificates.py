from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building

import numpy as np

class ESS__electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the Electricity Savings created from an Implementation?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"ESS Electricity Savings",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Energy Savings Scheme - General'
        }

    def formula(buildings, period, parameters):
        ESS_method_type = buildings('ESS__method_type', period)
        ESS_MethodType = (ESS_method_type.possible_values)
        NABERS_electricity_savings = buildings('ESS__NABERS_electricity_savings', period)
        electricity_savings = np.select([ESS_method_type == (ESS_MethodType.clause_8_8_NABERS),
                                         ESS_method_type == (ESS_MethodType.clause_9_8_HEER)],
                                         [NABERS_electricity_savings,
                                          0])
        return electricity_savings


class ESS__gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What are the Gas Savings created from an Implementation?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"ESS Gas Savings",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Energy Savings Scheme - General'
        }

    def formula(buildings, period, parameters):
        ESS_method_type = buildings('ESS__method_type', period)
        ESS_MethodType = (ESS_method_type.possible_values)
        NABERS_gas_savings = buildings('ESS__NABERS_gas_savings', period)
        gas_savings = np.select([ESS_method_type == (ESS_MethodType.clause_8_8_NABERS),
                                 ESS_method_type == (ESS_MethodType.clause_9_8_HEER)],
                                [NABERS_gas_savings,
                                 0])
        return gas_savings


class ESS__number_of_ESCs(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the number of ESCs created from an Implementation?'
    metadata={
        "variable-type": "inter-interesting",
        "alias":"ESS Number of Energy Savings Certificates",
        # "major-cat":"Energy Savings Scheme",
        # "monor-cat":'Energy Savings Scheme - General'
        }

    def formula(buildings, period, parameters):
        electricity_savings = buildings('ESS__electricity_savings', period)
        electricity_certificate_conversion_factor = parameters(period).ESS.ESS_general.ESS_certificate_conversion_factors.electricity_certificate_conversion_factor
        gas_savings = buildings('ESS__gas_savings', period)
        gas_certificate_conversion_factor = parameters(period).ESS.ESS_general.ESS_certificate_conversion_factors.gas_certificate_conversion_factor
        number_of_certificates =  np.floor((electricity_savings * electricity_certificate_conversion_factor)
                                            + (gas_savings * gas_certificate_conversion_factor))
        return number_of_certificates
