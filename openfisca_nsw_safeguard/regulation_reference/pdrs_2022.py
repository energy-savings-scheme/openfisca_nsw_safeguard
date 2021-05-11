from openfisca_nsw_safeguard.regulation_reference.regulation_reference import Regulation, PartType as PT


PDRS_2022 = Regulation(
    "PDRS 2022", "Peak Demand Reduction Scheme Rule 2022", "01 July 2022")

# Identify Common Variables---------------
generic_PDRS = PDRS_2022.add_part("XX", PT.NOTES, "Generic")
generic_PDRS_GA = generic_PDRS.add_part(
    "GA", PT.EQUIPMENT, "General Appliances")
generic_PDRS_AC = generic_PDRS.add_part("AC", PT.EQUIPMENT, "Air Conditioner")
generic_PDRS_motors = generic_PDRS.add_part(
    "motors", PT.EQUIPMENT, "Motors")

generic_PDRS_motors = generic_PDRS.add_part(
    "fridge", PT.EQUIPMENT, "Refrigerator or Freezer")


# Identify Methods and Activities---------------

HEAB = PDRS_2022.add_part(
    "HEAB", PT.SUBMETHOD, "High Efficiency Appliances For Business")
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
    "HEER", PT.SUBMETHOD, "Home Energy Efficiency Retrofits")
HEER.add_parts([
    ("AC_replace", PT.ACTIVITY,
     "Replace an Existing Air Conditioner With A High Efficiency Air Conditioner (non-business)"),
    ("AC_install", PT.ACTIVITY,
     "Install A High Efficiency Air Conditioner (non-business)"),
])


ROOA = PDRS_2022.add_part(
    "ROOA", PT.SUBMETHOD, "Removal Of Old Appliances")
ROOA.add_parts([
    ("fridge", PT.ACTIVITY, "Remove A Spare Refrigerator or Freezer"),
])
