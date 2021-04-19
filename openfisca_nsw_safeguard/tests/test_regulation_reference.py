import pytest

from openfisca_nsw_safeguard.regulation_reference._regulation_reference import Part, PartType, Regulation

def test_part_instantiation():
    # Incorrect instantiation raises error
    with pytest.raises(TypeError):
        test_part = Part()
    
    with pytest.raises(AttributeError):
        test_part = Part("A.1", "Not a PartType value", "Introduction")

    with pytest.raises(AttributeError):
        test_part = Part("A.1",  PartType.non_matching_key, "Introduction")
    
    # Correct instantiation passes
    test_part = Part("A.1", PartType.SUBCLAUSE, "Introduction")
    assert test_part.part_type.value == "Sub-clause"

def test_regulation_instantiation():
    # Incorrect instantiation raises error
    with pytest.raises(TypeError):
        test_ref = Regulation()

    # Correct instantiation passes
    test_ref = Regulation(name="TestRegulation", version="2020", commencement="01-Jan-2021")

def test_regulation_add_part():
    test_ref = Regulation(name="TestRegulation", version="2020", commencement="01-Jan-2021")
    test_ref.add_part(identifier="A.1", part_type=PartType.SUBCLAUSE, title="Introduction")


def test_regulation_add_parts():
    test_ref = Regulation(name="TestRegulation", version="2020", commencement="01-Jan-2021")

    parts = [("1", PartType.CLAUSE, "Name and Commencement"),
             ("1.1", PartType.SUBCLAUSE, "Definitions")
            ]
    test_ref.add_parts(parts)
