from openfisca_nsw_safeguard.regulation_reference.regulation_reference import Regulation, PartType as PT


PDRS_2022 = Regulation("PDRS 2022", "Peak Demand Reduction Scheme Rule 2022", "01 July 2022")

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
