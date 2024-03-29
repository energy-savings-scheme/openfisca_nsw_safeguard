# -*- coding: utf-8 -*-
import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_core.variables.variable import Variable

from openfisca_nsw_base import entities

# from openfisca_nsw_people import entities

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


# Our country tax and benefit class inherits from the general TaxBenefitSystem class.
# The name CountryTaxBenefitSystem must not be changed, as all tools of the OpenFisca
# ecosystem expect a CountryTaxBenefitSystem class to be exposed in the __init__ module of a country package.

class CountryTaxBenefitSystem(TaxBenefitSystem):
    def __init__(self):
        
        # We initialize our tax and benefit system with the general constructor
        super(CountryTaxBenefitSystem, self).__init__(entities.entities)
        # We add to our tax and benefit system all the variables
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))
        # We add to our tax and benefit system all the legislation parameters defined in the  parameters files
        param_path = os.path.join(COUNTRY_DIR, 'parameters')
        self.load_parameters(param_path)

        # We define which variable, parameter and simulation example will be used in the OpenAPI specification
        self.open_api_config = {
            "variable_example": "active_kids__child_meets_criteria",
            "parameter_example": "active_kids.min_age",
            }
