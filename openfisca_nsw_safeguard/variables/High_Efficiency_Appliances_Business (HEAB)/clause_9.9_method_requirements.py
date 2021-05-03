# # Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
# from openfisca_core.model_api import *
# # Import the Entities specifically defined for this tax and benefit system
# from openfisca_nsw_base.entities import *


# class installation_date(Variable):
#     value_type = date
#     entity = Building
#     definition_period = ETERNITY
#     label = 'The Implementation Date is the date that the End-User Equipment' \
#             ' is installed. As prescribed by Clause 9.9.1.'


# class energy_saver(Variable):
#     value_type = str
#     entity = Building
#     definition_period = ETERNITY
#     label = "The Energy Saver is the Purchaser. As prescribed in clause 9.9.3."

#     def formula(buildings, period, parameters):
#         purchaser = buildings('purchaser', period)
#         return purchaser


# class purchaser(Variable):
#     value_type = str
#     entity = Building
#     definition_period = ETERNITY
#     label = "The Purchaser of the site, as defined in Clause 10.1."


# class purchaser_is_eligible(Variable):
#     value_type = bool
#     entity = Building
#     definition_period = ETERNITY
#     label = 'Asks whether the Purchaser meets the condition of being a' \
#             ' Purchaser, as defined in Clause 10.1.'

#     def formula(buildings, period, parameters):
#         purchaser_is_ACP = buildings('purchaser_is_ACP', period)
#         purchaser_is_owner = buildings('purchaser_is_owner', period)
#         purchaser_is_occupier = buildings('purchaser_is_occupier', period)
#         purchaser_is_operator = buildings('purchaser_is_operator', period)
#         return purchaser_is_ACP * ((not(purchaser_is_owner)) + (not(purchaser_is_occupier)) + (not(purchaser_is_operator)))


# class purchaser_is_ACP(Variable):
#     value_type = bool
#     entity = Building
#     definition_period = ETERNITY
#     label = 'Asks whether the Purchaser is the ACP.'


# class purchaser_is_owner(Variable):
#     value_type = bool
#     entity = Building
#     definition_period = ETERNITY
#     label = 'Asks whether the Purchaser is the owner.'


# class purchaser_is_occupier(Variable):
#     value_type = bool
#     entity = Building
#     definition_period = ETERNITY
#     label = 'Asks whether the Purchaser is the occupier.'


# class purchaser_is_operator(Variable):
#     value_type = bool
#     entity = Building
#     definition_period = ETERNITY
#     label = 'Asks whether the Purchaser is the operator.'
