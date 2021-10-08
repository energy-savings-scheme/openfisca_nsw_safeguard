from openfisca_core.variables import Variable
from openfisca_core.periods import ETERNITY
from openfisca_core.indexed_enums import Enum
from openfisca_nsw_base.entities import Building


class ESS_HEER_install_external_blind_new_equipment_is_external_shading_device(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new product is an external shading device' \
            ' as prescribed in Equipment Requirement 1.'


class ESS_HEER_install_external_blind_new_equipment_is_automated(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the new product is automated.'


class ESS_HEER_install_external_blind_minimum_warranty_length(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the blind has a minimum warranty length of' \
            ' 5 years, as required by Equipment Requirement 3.'

    def formula(buildings, period, parameters):
        warranty_length = buildings('ESS_HEER_new_product_warranty_length', period)
        return warranty_length >= 5


class ESS_HEER_install_external_blind_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the Implementation meets the Equipment Requirements' \
            ' defined in Activity Definition E10.'

    def formula(buildings, period, parameters):
        is_external_shading_device = buildings(
        'ESS_HEER_install_external_blind_new_equipment_is_external_shading_device', period)
        new_product_is_automated = buildings(
        'ESS_HEER_install_external_blind_new_equipment_is_automated', period)
        has_minimum_warranty_length = buildings(
        'ESS_HEER_install_external_blind_minimum_warranty_length', period)
        return (
                is_external_shading_device *
                new_product_is_automated *
                has_minimum_warranty_length
                )
