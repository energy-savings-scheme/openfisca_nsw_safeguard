from openfisca_nsw_safeguard.regulation_reference.regulation_reference import Regulation, PartType as PT


ESS_2021 = Regulation("ESS 2021", "Energy Savings Scheme (Amendment No. 1) Rule 2021", "01 May 2021")

clause_8 = ESS_2021.add_part("8", PT.CLAUSE, "Metered Baseline Method")
clause_8.add_parts([("1", PT.CLAUSE, None),
                  ("2", PT.CLAUSE, None),
                  ("3", PT.CLAUSE, None),
                  ("3.A", PT.CLAUSE, None),
                  ("4", PT.CLAUSE, None),
                  ("4.A", PT.CLAUSE, "Additional Requirements for Lighting Upgrades"),
                  ("4.B", PT.CLAUSE, "Acceptable End-User Equipment for Lighting Upgrades"),
                  ("5", PT.CLAUSE, "Baseline Per Unit of Output"),
                  ("6", PT.CLAUSE, "Baseline Unaffected by Output"),
                  ("7", PT.CLAUSE, "Normalised Baseline"),
                  ("8", PT.CLAUSE, "NABERS Baseline"),
                  ("9", PT.CLAUSE, "Aggregated Metered Baseline")])

clause_9 = ESS_2021.add_part("9", PT.CLAUSE, "Deemed Energy Savings Method")
clause_9.add_parts([("1", PT.CLAUSE, None),
                  ("2", PT.CLAUSE, None),
                  ("2.A", PT.CLAUSE, "Acceptable End-User Equipment"),
                  ("3", PT.CLAUSE, "Sale of New Appliances")
               ])

schedule_B = ESS_2021.add_part("B", PT.SCHEDULE, "Activity Definitions for the Sale of New Appliances")
schedule_B.add_parts([
                     ("1", PT.ACTIVITY, "Sell a High Efficiency Clothes Washing Machine"),
                     ("2", PT.ACTIVITY, "Sell a High Efficiency Clothes Dryer")
                     ])    
