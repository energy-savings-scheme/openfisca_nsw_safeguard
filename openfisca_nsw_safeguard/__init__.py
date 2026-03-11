# -*- coding: utf-8 -*-
import os
import numpy
import typing

from openfisca_core.taxscales import SingleAmountTaxScale
from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_web_api.loader import variables

from openfisca_nsw_safeguard.entities import entities

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


def custom_calc(self,
        tax_base: typing.Union[numpy.int_, numpy.float_],
        right: bool = False,
        interpolate: bool = False,
        interp_right: typing.Union[numpy.int_, numpy.float_, None] = None,
        interp_left: typing.Union[numpy.int_, numpy.float_, None] = None
    ) -> numpy.float_:
        """
        Matches the input amount to a set of brackets and returns the single
        cell value that fits within that bracket.
        """
        if interpolate:
             thresholds = self.thresholds
             amounts = self.amounts
             result = numpy.interp(tax_base, thresholds, amounts, left=interp_left, right=interp_right)
             return result
        else:
            guarded_thresholds = numpy.array([-numpy.inf] + self.thresholds + [numpy.inf])

            bracket_indices = numpy.digitize(
                tax_base,
                guarded_thresholds,
                right=right,
            )

            guarded_amounts = numpy.array([0] + self.amounts + [0])

            return guarded_amounts[bracket_indices - 1]


_original_build_variable = variables.build_variable
def custom_build_variable(variable, country_package_metadata):
    result = _original_build_variable(variable, country_package_metadata)
    result["metadata"] = variable.metadata
    return result

# We did monkey patch here in order to implement our own logic
# to replace cacl method in class SingleAmountTaxScale
# the custom_calc function is modified version from calc method of openfisca core
# the custom_build_variable function is extended version from function build_variable
# specifically openfisca core 40.0.1
SingleAmountTaxScale.calc = custom_calc
variables.build_variable = custom_build_variable


# Our country tax and benefit class inherits from the general TaxBenefitSystem class.
# The name CountryTaxBenefitSystem must not be changed, as all tools of the OpenFisca
# ecosystem expect a CountryTaxBenefitSystem class to be exposed in the __init__ module of a country package.

class CountryTaxBenefitSystem(TaxBenefitSystem):
    def __init__(self):
        
        # We initialize our tax and benefit system with the general constructor
        super(CountryTaxBenefitSystem, self).__init__(entities)
        # We add to our tax and benefit system all the variables
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))
        # We add to our tax and benefit system all the legislation parameters defined in the  parameters files
        param_path = os.path.join(COUNTRY_DIR, 'parameters')
        self.load_parameters(param_path)

        # We define which variable, parameter and simulation example will be used in the OpenAPI specification
        # self.open_api_config = {
        #     "variable_example": "active_kids__child_meets_criteria",
        #     "parameter_example": "active_kids.min_age",
        # }
