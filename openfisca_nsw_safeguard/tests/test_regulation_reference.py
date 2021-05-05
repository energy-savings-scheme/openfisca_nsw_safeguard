import pytest
from openfisca_nsw_safeguard.regulation_reference.regulation_reference import Regulation, PartType as PT


def test_regulation_reference():
    # Test instantiation of Regulation object
    ESS_2020 = Regulation("ESS 2020", "1 July 2020",
                          "26 June 2020")

    clause_9 = ESS_2020.add_part(
        "9", PT.CLAUSE, "Deemed Energy Savings Method")
    clause_9_1 = clause_9.add_part("1", PT.CLAUSE, None)
    clause_9_2 = clause_9.add_part("2", PT.CLAUSE, None)
    clause_9_2A = clause_9.add_part(
        "2.A", PT.CLAUSE, "Acceptable End-User Equipment")
    clause_9_3 = clause_9.add_part("3", PT.CLAUSE, "Sale of New Appliances")

    schedule_B = ESS_2020.add_part(
        "B", PT.SCHEDULE, "Activity Definitions for the Sale of New Appliances")
    activity_B1 = schedule_B.add_part(
        "1", PT.ACTIVITY, "Sell a High Efficiency Clothes Washing Machine")
    activity_B2 = schedule_B.add_part(
        "2", PT.ACTIVITY, "Sell a High Efficiency Clothes Dryer")

    # Test accessing of Regulation object
    accessor = ESS_2020["B", "1"]
    assert accessor["identifier"] == "ESS 2020"
    assert accessor["part"]["identifier"] == "B"

    # Test invalid accessor raises error
    with pytest.raises(KeyError):
        invalid = ESS_2020["C", "1"]
