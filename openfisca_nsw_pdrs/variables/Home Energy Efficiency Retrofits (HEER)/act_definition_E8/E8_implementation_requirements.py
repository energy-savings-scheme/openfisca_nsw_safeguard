# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class product_applied_to_window_sash_perimeter(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Product is applied to the perimeter of the window sash.' \
            ' As prescribed by Implementation Requirement 1.'


class E8_product_restricts_airflow(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product effectively restricts airflow into or' \
            ' out of the site around the perimeter of the Door, as required' \
            ' in Implementation Requirement 2.'


class E8_product_installed_according_to_instructions(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product has been installed in strict accordance' \
            ' with the manufacturer instructions, as prescribed by' \
            ' Implementation Requirement 3.'


class all_external_windows_are_draught_proofed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether all windows on the Site that meet the Eligibility' \
            ' Requirements, excluding sliding doors have been draught proofed,' \
            ' in accordance with Implementation Requirement 4.'  # this means you need to run the eligibility requirement for every door on the size and probably have a flag saying


class installed_in_accordance_with_BCA (Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the window is installed with National Construction' \
            ' Code BCA Section J3 and any relevant AS/NZS as required by the' \
            ' Scheme Administrator.'
