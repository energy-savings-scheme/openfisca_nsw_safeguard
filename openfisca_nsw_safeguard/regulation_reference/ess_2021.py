from openfisca_nsw_safeguard.regulation_reference.regulation_reference import Regulation, PartType as PT


ESS_2021 = Regulation(
    "ESS 2021", "Energy Savings Scheme (Amendment No. 1) Rule 2021", "01 May 2021")

# Identify Common Variables---------------
generic_ESS = ESS_2021.add_part("XX", PT.EQUIPMENT, "Generic")
generic_ESS_GA = generic_ESS.add_part("GA", PT.EQUIPMENT, "General Appliances")
generic_ESS_AC = generic_ESS.add_part("AC", PT.EQUIPMENT, "Air Conditioner")


#  Variables Specific to Clauses ---------------

clause_8 = ESS_2021.add_part("8", PT.CLAUSE, "Metered Baseline Method")
clause_8.add_parts([("8.1", PT.CLAUSE, None),
                    ("8.2", PT.CLAUSE, None),
                    ("8.3", PT.CLAUSE, None),
                    ("8.3.A", PT.CLAUSE, None),
                    ("8.4", PT.CLAUSE, None),
                    ("8.4.A", PT.CLAUSE, "Additional Requirements for Lighting Upgrades"),
                    ("8.4.B", PT.CLAUSE,
                     "Acceptable End-User Equipment for Lighting Upgrades"),
                    ("8.5", PT.ACTIVITY, "Baseline Per Unit of Output"),
                    ("8.6", PT.ACTIVITY, "Baseline Unaffected by Output"),
                    ("8.7", PT.ACTIVITY, "Normalised Baseline"),
                    ("8.8", PT.ACTIVITY, "NABERS Baseline"),
                    ("8.9", PT.ACTIVITY, "Aggregated Metered Baseline")])

clause_9 = ESS_2021.add_part("9", PT.CLAUSE, "Deemed Energy Savings Method")
clause_9.add_parts([("9.1", PT.CLAUSE, None),
                    ("9.2", PT.CLAUSE, None),
                    ("9.2.A", PT.CLAUSE, "Acceptable End-User Equipment"),
                    ("9.3", PT.CLAUSE, "Sale of New Appliances"),
                    ("9.6", PT.CLAUSE, "Power Factor Correction"),
                    ("9.8", PT.CLAUSE, "Home Energy Efficiency Retrofits"),
                    ("9.9", PT.CLAUSE,
                     "Installation of High Efficiency Appliances for Business"),
                    ])

schedule_B = ESS_2021.add_part(
    "B", PT.SCHEDULE, "Activity Definitions for the Sale of New Appliances")
schedule_B.add_parts([
                     ("B1", PT.ACTIVITY, "Sell a High Efficiency Clothes Washing Machine"),
                     ("B2", PT.ACTIVITY, "Sell a High Efficiency Clothes Dryer"),
                     ("B3", PT.ACTIVITY, "Sell a High Efficiency Dishwasher"),
                     ("B4", PT.ACTIVITY, "Sell a High Efficiency 1-Door Refrigerator"),
                     ("B5", PT.ACTIVITY, "Sell a High Efficiency Refrigerator with 2 or More Doors"),
                     ("B6", PT.ACTIVITY, "Sell a High Efficiency Chest Freezer or Upright Freezer"),
                     ("B7", PT.ACTIVITY, "Sell a High Efficiency Television")
                     ])

schedule_C = ESS_2021.add_part(
    "C", PT.SCHEDULE, "Activity Definitions for the Removal of Old Appliances")
schedule_C.add_parts([
                     ("C1", PT.ACTIVITY, "Remove a Spare Refrigerator or Freezer"),
                     ("C2", PT.ACTIVITY, "Remove a Primary Refrigerator or Freezer")
                     ])

schedule_D = ESS_2021.add_part(
    "D", PT.SCHEDULE, "Activity Definitions for General Activities for Home Energy Efficiency Retrofits")
schedule_D.add_parts([
                     ("D1", PT.ACTIVITY, "Replace an External Single Glazed Window or Door with a Thermally Efficient Window or Door"),
                     ("D2", PT.ACTIVITY, "Modify an External Window or Glazed Door by Installing Secondary Glazing"),
                     ("D5", PT.ACTIVITY, "Replace an Existing Pool Pump with a High Efficiency Pool Pump"),
                     ("D6", PT.ACTIVITY, "Install Ceiling Insulation in an Uninsulated Ceiling Place"),
                     ("D7", PT.ACTIVITY, "Install Ceiling Insulation in an Under-insulated Ceiling Place"),
                     ("D8", PT.ACTIVITY, "Install Under-floor Insulation"),
                     ("D9", PT.ACTIVITY, "Install Wall Insulation"),
                     ("D11", PT.ACTIVITY, "Replace an Existing Gas-fired Water Heater with a High Efficiency Gas Fired Water Heater"),
                     ("D12", PT.ACTIVITY, "Install a High Efficiency Gas Space Heater or Replace an Existing Gas Space Heater with" \
                     " a High Efficiency Gas Space Heater"),
                     ("D13", PT.ACTIVITY, "Install a Natural Roof Space Ventilator"),
                     ("D14", PT.ACTIVITY, "Install a Fan-forced Roof Space Ventilator, PV Powered Fan-forced Space Ventilator" \
                     " or an Occupied Space Ventilator"),
                     ("D15", PT.ACTIVITY, "Replace an Exhaust Fan with a Self Sealing Exhaust Fan"),
                     ("D16", PT.ACTIVITY, "Install a New High Efficiency Air Conditioner or Replace an Existing Air Conditioner" \
                     " with a High Efficiency Air Conditioner"),
                     ("D17", PT.ACTIVITY, "Replace an Existing Electric Water Heater with an (Air Source) Heat Pump Water Heater"),
                     ("D18", PT.ACTIVITY, "Replace an Existing Electric Water Heater with a Solar (Electric Boosted) Water Heater"),
                     ("D19", PT.ACTIVITY, "Replace an Existing Gas Water Heater with an Air Source Heat Pump Water Heater"),
                     ("D20", PT.ACTIVITY, "Replace an Existing Gas Water Heater with a Solar (Electric Boosted) Water Heater"),
                     ("D21", PT.ACTIVITY, "Replace an Existing Gas Water Heater with a Solar (Gas Boosted) Water Heater"),
                     ])

schedule_E = ESS_2021.add_part(
    "E", PT.SCHEDULE, "Activity Definitions for Low Cost Activites for High Efficiency Appliances for Businesses (clause 9.8)")
schedule_E.add_parts([
                     ("E1", PT.ACTIVITY, "Replace Halogen Downlight with LED Luminaire and/or Lamp"),
                     ("E2", PT.ACTIVITY, "Replace a Linear Halogen Floodlight with a High Efficiency Lamp"),
                     ("E3", PT.ACTIVITY, "Replace a Parabolic Aluminised Reflector (PAR) Lamp with Efficient Luminaire and/or Lamp"),
                     ("E4", PT.ACTIVITY, "Replace a T8 or T12 Luminaire with a T5 Luminaire"),
                     ("E5", PT.ACTIVITY, "Replace a T8 or T12 Luminaire with an LED Luminaire"),
                     ("E6", PT.ACTIVITY, "Replace an Existing Showerhead with an Ultra Low Flow Showerhead"),
                     ("E7", PT.ACTIVITY, "Modify an External Door with Draught Proofing"),
                     ("E8", PT.ACTIVITY, "Modify an External Window with Draught Proofing"),
                     ("E9", PT.ACTIVITY, "Modify a Fireplace Chimney by Sealing with a Damper"),
                     ("E10", PT.ACTIVITY, "Install an External Blind to a Window or Door"),
                     ("E11", PT.ACTIVITY, "Replace an Edison Screw or Bayonet Lamp with an LED Lamp for General Lighting Purposes"),
                     ("E12", PT.ACTIVITY, "Modify an Exhaust Fan with a Sealing Product"),
                     ("E13", PT.ACTIVITY, "Replace a T5 Luminaire with a LED Luminaire"),
                     ])



schedule_F = ESS_2021.add_part(
    "F", PT.SCHEDULE, "Activity Definitions for Installation of High Efficiency Appliances for Businesses (clause 9.9)")
schedule_F.add_parts([
                     ("F4", PT.ACTIVITY, "Install A New High Efficiency Air Conditioner"),
                     ("F7", PT.ACTIVITY, "Install a New High Efficiency Motor")
                     ])
