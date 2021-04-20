from openfisca_nsw_safeguard.regulation_reference.regulation_reference import Regulation, PartType as PT


PDRS_2022 = Regulation("PDRS 2022", "Peak Demand Reduction Scheme Rule 2022", "01 July 2022")

clause_8 = PDRS_2022.add_part("8", PT.CLAUSE, "Example")
clause_8.add_parts([("1", PT.CLAUSE, None),
                  ("2", PT.CLAUSE, None),
                  ("3", PT.CLAUSE, None),
                  ("3.A", PT.CLAUSE, None),
                  ("4", PT.CLAUSE, None),
                  ("4.A", PT.CLAUSE, "Example ABC"),
                  ("4.B", PT.CLAUSE, "Example DEF"),
                  ("5", PT.CLAUSE, "Example GHI"),
                  ("6", PT.CLAUSE, "Example JKL"),
                  ("7", PT.CLAUSE, "Example MNO"),
                  ("8", PT.CLAUSE, "Example PQR"),
                  ("9", PT.CLAUSE, "Example STU"),
])
