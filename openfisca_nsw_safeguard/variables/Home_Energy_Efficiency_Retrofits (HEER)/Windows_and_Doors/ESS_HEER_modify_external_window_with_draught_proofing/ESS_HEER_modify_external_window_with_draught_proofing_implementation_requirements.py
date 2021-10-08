from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS_HEER_modify_external_window_with_draught_proofing_product_applied_to_window_sash_perimeter(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Product is applied to the perimeter of the window sash.' \
            ' As prescribed by Implementation Requirement 1.'


class ESS_HEER_modify_external_window_with_draught_proofing_product_restricts_airflow(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product effectively restricts airflow into or' \
            ' out of the site around the perimeter of the Door, as required' \
            ' in Implementation Requirement 2.'


class ESS_HEER_modify_external_window_with_draught_proofing_product_installed_according_to_instructions(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product has been installed in strict accordance' \
            ' with the manufacturer instructions, as prescribed by' \
            ' Implementation Requirement 3.'


class ESS_HEER_modify_external_window_with_draught_proofing_all_external_windows_are_draught_proofed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether all windows on the Site that meet the Eligibility' \
            ' Requirements, excluding sliding doors have been draught proofed,' \
            ' in accordance with Implementation Requirement 4.'  # this means you need to run the eligibility requirement for every door on the size and probably have a flag saying


class ESS_HEER_modify_external_window_with_draught_proofing_installed_in_accordance_with_BCA(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the window is installed with National Construction' \
            ' Code BCA Section J3 and any relevant AS/NZS as required by the' \
            ' Scheme Administrator.'


class ESS_HEER_modify_external_window_with_draught_proofing_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the Implementation meets the Implementation Requirements defined in' \
            ' Activity Definition E8.'

    def formula(buildings, period, parameters):
        product_applied_to_perimeter = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_product_applied_to_window_sash_perimeter', 
            period)
        product_effectively_restricts_airflow = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_product_restricts_airflow', 
            period)
        product_installed_to_instructions = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_product_installed_according_to_instructions', 
            period)
        all_windows_are_draught_proofed = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_all_external_windows_are_draught_proofed', 
            period)
        installed_in_accordance_to_BCA = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_installed_in_accordance_with_BCA',
            period)
        return(
            product_applied_to_perimeter *
            product_effectively_restricts_airflow *
            product_installed_to_instructions *
            all_windows_are_draught_proofed *
            installed_in_accordance_to_BCA
        )