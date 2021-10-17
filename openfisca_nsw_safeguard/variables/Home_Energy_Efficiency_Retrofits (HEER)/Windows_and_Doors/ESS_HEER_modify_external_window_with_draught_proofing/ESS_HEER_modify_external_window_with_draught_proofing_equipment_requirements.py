from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_nsw_base.entities import Building


class ESS_HEER_modify_external_window_with_draught_proofing_new_equipment_is_window_sealing_product(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new product is a retail window sealing product.'


class ESS_HEER_modify_external_window_with_draught_proofing_new_equipment_is_weather_stripping_product(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new product is a weather stripping product.'


class ESS_HEER_modify_external_window_with_draught_proofing_new_equipment_is_eligible_product(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product that is applied is a retail door bottom' \
            ' sealing product or door perimeter weather stripping product,' \
            ' as prescribed by Equipment Requirement 1.'

    def formula(buildings, period, parameters):
        window_sealing_product = buildings('new_equipment_is_window_sealing_product', period)
        window_weather_sealing_product = buildings('new_equipment_is_weather_stripping_product', period)
        return window_sealing_product + window_weather_sealing_product


class ESS_HEER_modify_external_window_with_draught_proofing_new_equipment_is_fit_for_purpose(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product is fit for purpose, as prescribed by' \
            ' Equipment Requirement 2.'  # IPART to define what this means


class ESS_HEER_modify_external_window_with_draught_proofing_sealing_surface_material_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'The product’s sealing surface must be made of a durable' \
            ' compressible material such as foam, polypropylene pile,' \
            ' flexible plastic, rubber compressible strip, fibrous' \
            ' seal or similar. As prescribed by Equipment Requirement 3.'


class ESS_HEER_modify_external_window_with_draught_proofing_new_equipment_does_not_impair_window_operation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the product does not impair the operation of the' \
            ' relevant window.'  # IPART to define what this means


class ESS_HEER_modify_external_window_with_draught_proofing_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the sealing product has a minimum warranty length of' \
            ' 2 years, as required by Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('ESS_HEER_new_product_warranty_length', period)
        return warranty_length >= 2 # need to eventually rewrite as parameter


class ESS_HEER_modify_external_window_with_draught_proofing_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the Implementation meets the Equipment Requirements' \
            ' as detailed in Activity Definition E8.'

    def formula(buildings, period, parameters):
        new_product_is_eligible = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_new_equipment_is_eligible_product',
            period)
        new_product_is_fit_for_purpose = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_new_equipment_is_fit_for_purpose', 
            period)
        surface_material_is_eligible = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_sealing_surface_material_is_eligible',
            period)
        window_operation_is_not_impaired = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_new_equipment_does_not_impair_window_operation',
            period)
        has_minimum_warranty = buildings(
            'ESS_HEER_modify_external_window_with_draught_proofing_minimum_warranty_length', period
            )
        return(
            new_product_is_eligible *
            new_product_is_fit_for_purpose *
            surface_material_is_eligible *
            window_operation_is_not_impaired *
            has_minimum_warranty
        )