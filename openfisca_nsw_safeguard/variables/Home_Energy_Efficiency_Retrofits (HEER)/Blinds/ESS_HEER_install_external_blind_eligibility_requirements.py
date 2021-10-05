# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class ESS_HEER_install_external_blind_site_must_be_residential_or_small_building(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'The External Blind must be installed to a door or window' \
            ' in a Residential or Small Building Site, as prescribed in ' \
            ' Eligiblity Requirement 1. '  # IPART to define what this means and how to measure this. need to build building type enum and refer into this

    def formula(buildings, period, parameters):
        site_type = buildings('ESS_site_type', period)
        ESS_SiteType = site_type.possible_values
        is_residential = (site_type == ESS_SiteType.residential)
        is_small_business = (site_type == ESS_SiteType.small_business)
        return(
        is_residential *
        is_small_business
        )


class ESS_HEER_install_external_blind_window_or_door_is_fully_glazed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the door or window for which the blind is installed' \
            ' on is fully glazed, as prescribed in Eligibility Requirement 2.'


class ESS_HEER_install_external_blind_window_or_door_does_not_face_south(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'The window or door must not face south, between 135 and 225' \
            ' degrees of true north, as prescribed in Eligibility Requirement' \
            ' 3.'

    def formula(buildings, period, parameters):
        orientation = buildings('ESS_HEER_install_external_blind_window_or_door_orientation', period)
        condition_degrees_from_true_north = (
                                            (orientation >= 135) *
                                            (orientation <= 225)
                                            )
        return not(condition_degrees_from_true_north)


class ESS_HEER_install_external_blind_window_or_door_orientation(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the orientation of the window or door, in degrees from' \
            ' true north.'


class ESS_HEER_install_external_blind_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the Implementation meets the Eligibility Requirements' \
            ' detailed in Activity Definition E10.'

    def formula(buildings, period, parameters):
        site_is_residential_or_small_business = buildings(
        'ESS_HEER_install_external_blind_site_must_be_residential_or_small_building', period)
        door_or_window_is_fully_glazed = buildings(
        'ESS_HEER_install_external_blind_window_or_door_is_fully_glazed', period)
        door_does_not_face_south = buildings(
        'ESS_HEER_install_external_blind_window_or_door_does_not_face_south', period)
        return (
        site_is_residential_or_small_business *
        door_or_window_is_fully_glazed *
        door_does_not_face_south
        )
