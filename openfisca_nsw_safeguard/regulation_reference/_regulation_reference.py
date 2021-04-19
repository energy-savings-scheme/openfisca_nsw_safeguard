""" The "RegulationReference" object is a structured Python object which
defines a reference to the legislation text

Intended use:
- Intended to be used in a Variable's `metadata["regulation_reference"]` key.

Usage notes:
- RegulationReference objects are instantiated in this file and imported
  into other modules.
- RegulationReference objects serialise to stringified JSON

"""

import json
from enum import Enum


class PartType(Enum):
    PART = "Part"
    CLAUSE = "Clause"
    SUBCLAUSE = "Sub-clause"
    SCHEDULE = "Schedule"
    ACTIVITY_DEFINITION = "Activity definition"
    NOTES = "Notes"


class _Part:

    __jsonkeys__ = ('identifier', 'part_type', 'title')

    def __init__(self, identifier, part_type, title):
        self.identifier = identifier
        self.part_type = part_type
        self.title = title
        self._parts = {}

    def add_part(self, *args, **kwargs):
        new_part = _Part(*args, **kwargs)
        self._parts[new_part.identifier] = new_part
        return new_part

    def add_parts(self, parts):
        for part in parts:
            self.add_part(*part)

    def json(self):
        return json.dumps(self)

    def __getitem__(self, key):
        return self._PartView(self, key)

    class _PartView:
        def __init__(self, part, keys):
            self._part = part
            if tuple(keys):
                child = part._parts[keys[0]]
                self._child = type(self)(child, keys[1:])
            else:
                self._child = None

        @property
        def part(self):
            return self._child

        @property
        def __jsonkeys__(self):
            return (self._part.__jsonkeys__ + (('part',)
                    if self._child is not None else ()))

        def __getattr__(self, name):
            return getattr(self._part, name)

        def render(self):
            return json.loads(json.dumps(self, cls=_JSONEncoder))

class Part:
    def __init__(self, identifier, part_type, title):
        if not isinstance(part_type, PartType):
            raise AttributeError("`part_type` argument must be an Enum value of PartType (e.g. `PartType.CLAUSE`")

        self.identifier = identifier
        self.part_type = part_type
        self.title = title


class Regulation:

    def __init__(self, name, version, commencement):

        self.identifier = name
        self.version = version
        self.commencement = commencement

        self._parts = []

    def add_parts(self, parts):
        for part in parts:
            self.add_part(*part)

    def add_part(self, *args, **kwargs):
        self._parts.append(Part(*args, **kwargs))