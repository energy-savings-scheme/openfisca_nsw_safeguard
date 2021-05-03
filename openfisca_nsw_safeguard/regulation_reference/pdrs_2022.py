from openfisca_nsw_safeguard.regulation_reference.regulation_reference import Regulation, PartType as PT


PDRS_2022 = Regulation(
    "PDRS 2022", "Peak Demand Reduction Scheme Rule 2022", "01 July 2022")

clause_8 = PDRS_2022.add_part("X", PT.CLAUSE, "PDRS Method (example)")
clause_8.add_parts([("X.1", PT.CLAUSE, None),
                    ("X.2", PT.CLAUSE, None),
                    ("X.3", PT.CLAUSE, None),
                    ("X.3.A", PT.CLAUSE, None),
                    ("X.4", PT.CLAUSE, None),
                    ("X.4.A", PT.CLAUSE, "Example ABC"),
                    ("X.4.B", PT.CLAUSE, "Example DEF"),
                    ("X.5", PT.ACTIVITY, "PDRS Air Conditioners"),
                    ("X.6", PT.ACTIVITY, "PDRS Motors"),
                    ("X.7", PT.ACTIVITY, "PDRS Removal of Old Appliances"),
                    ])


schedule_D = ESS_2021.add_part(
    "D", PT.SCHEDULE, "Activity Definitions for General Activities for Home Energy Efficiency Retrofits")
schedule_D.add_parts([
                     ("D1", PT.ACTIVITY, "Replace an External Single Glazed Window or Door with a Thermally Efficient Window or Door"),
                     ("D3", PT.ACTIVITY, "Replace an Existing Air Conditioner With A High Efficiency Air Conditioner"),
                     ("D4", PT.ACTIVITY, "Install A High Efficiency Air Conditioner"),
                     ("D16", PT.ACTIVITY, "Install a New High Efficiency Air Conditioner or Replace an Existing Air Conditioner with a High Efficiency Air Conditioner")
                     ])


schedule_F = ESS_2021.add_part(
    "F", PT.SCHEDULE, "Activity Definitions for Installation of High Efficiency Appliances for Businesses (clause 9.9)")
schedule_F.add_parts([
                     ("F4", PT.ACTIVITY, "Install A New High Efficiency Air Conditioner
                      "),
                     ("F7", PT.ACTIVITY, "Install a New High Efficiency Motor")
                     ])
