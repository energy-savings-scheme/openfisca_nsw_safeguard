from openfisca_nsw_safeguard.regulation_reference.regulation_reference import Regulation, PartType as PT


PDRS_2022 = Regulation(
    "PDRS 2022", "Peak Demand Reduction Scheme Rule 2022", "01 July 2022")

# Identify Common Variables---------------
generic_PDRS = PDRS_2022.add_part("XX", PT.NOTES, "Generic")
generic_PDRS_GA = generic_PDRS.add_part(
    "GA", PT.NOTES, "PDRS General Appliances")
generic_PDRS_AC = generic_PDRS.add_part("AC", PT.NOTES, "PDRS Air Conditioner")
generic_PDRS_motors = generic_PDRS.add_part(
    "motors", PT.NOTES, "PDRS motors")

generic_PDRS_motors = generic_PDRS.add_part(
    "fridge", PT.NOTES, "PDRS fridge")

# clause_8 = PDRS_2022.add_part("X", PT.CLAUSE, "PDRS Method (example)")
# clause_8.add_parts([("X.1", PT.CLAUSE, None),
#                     ("X.2", PT.CLAUSE, None),
#                     ("X.3", PT.CLAUSE, None),
#                     ("X.3.A", PT.CLAUSE, None),
#                     ("X.4", PT.CLAUSE, None),
#                     ("X.4.A", PT.CLAUSE, "Example ABC"),
#                     ("X.4.B", PT.CLAUSE, "Example DEF"),
#                     ("X.5", PT.ACTIVITY, "PDRS Air Conditioners"),
#                     ("X.6", PT.ACTIVITY, "PDRS Motors"),
#                     ("X.7", PT.ACTIVITY, "PDRS Removal of Old Appliances"),
#                     ])


# Identify Methods and Activities---------------

HEAB = PDRS_2022.add_part(
    "HEAB", PT.SCHEDULE, "High Efficiency Appliances For Business")
HEAB.add_parts([
    ("AC_replace", PT.ACTIVITY,
     "Replace an Existing Air Conditioner With A High Efficiency Air Conditioner for Business"),
    ("AC_install", PT.ACTIVITY,
     "Install A High Efficiency Air Conditioner for Business"),
    ("motors_install", PT.ACTIVITY,
     "Install High Efficiency Motors"),
    ("motors_replace", PT.ACTIVITY,
     "Replace High Efficiency Motors"),
])


HEER = PDRS_2022.add_part(
    "HEER", PT.SCHEDULE, "Home Energy Efficiency Retrofits")
HEER.add_parts([
    ("AC_install", PT.ACTIVITY,
     "Replace an Existing Air Conditioner With A High Efficiency Air Conditioner (non-business)"),
    ("AC_install", PT.ACTIVITY,
     "Install A High Efficiency Air Conditioner (non-business)"),
])


ROOA = PDRS_2022.add_part(
    "ROOA", PT.SCHEDULE, "")
ROOA.add_parts([
    ("fridge", PT.ACTIVITY, "Remove A Spare Refrigerator or Freezer"),
])
