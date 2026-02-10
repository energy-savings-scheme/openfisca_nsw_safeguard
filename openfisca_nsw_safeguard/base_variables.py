from openfisca_core import periods
from openfisca_core.variables.variable import Variable
from openfisca_core.indexed_enums import Enum
from openfisca_core.variables import config, helpers
from openfisca_core.periods import DateUnit


# This BaseVariable class constructor is based on Openfisca Core
# We currently using constructor from class Variable
# specifically openfisca core 40.0.1
# and add the metadata block code for our needs right now.
class BaseVariable(Variable):
    def __init__(self, baseline_variable=None) -> None:
        self.name = self.__class__.__name__
        attr = {
            name: value
            for name, value in self.__class__.__dict__.items()
            if not name.startswith("__")
        }
        self.baseline_variable = baseline_variable
        self.value_type = self.set(
            attr,
            "value_type",
            required=True,
            allowed_values=config.VALUE_TYPES.keys(),
        )
        self.dtype = config.VALUE_TYPES[self.value_type]["dtype"]
        self.json_type = config.VALUE_TYPES[self.value_type]["json_type"]
        if self.value_type == Enum:
            self.possible_values = self.set(
                attr,
                "possible_values",
                required=True,
                setter=self.set_possible_values,
            )
        if self.value_type == str:
            self.max_length = self.set(attr, "max_length", allowed_type=int)
            if self.max_length:
                self.dtype = f"|S{self.max_length}"
        if self.value_type == Enum:
            self.default_value = self.set(
                attr,
                "default_value",
                allowed_type=self.possible_values,
                required=True,
            )
        else:
            self.default_value = self.set(
                attr,
                "default_value",
                allowed_type=self.value_type,
                default=config.VALUE_TYPES[self.value_type].get("default"),
            )
        self.entity = self.set(attr, "entity", required=True, setter=self.set_entity)
        self.definition_period = self.set(
            attr,
            "definition_period",
            required=True,
            allowed_values=DateUnit,
        )
        self.label = self.set(attr, "label", allowed_type=str, setter=self.set_label)
        self.end = self.set(attr, "end", allowed_type=str, setter=self.set_end)
        self.reference = self.set(attr, "reference", setter=self.set_reference)
        self.cerfa_field = self.set(attr, "cerfa_field", allowed_type=(str, dict))
        self.unit = self.set(attr, "unit", allowed_type=str)
        self.documentation = self.set(
            attr,
            "documentation",
            allowed_type=str,
            setter=self.set_documentation,
        )
        self.set_input = self.set_set_input(attr.pop("set_input", None))
        self.calculate_output = self.set_calculate_output(
            attr.pop("calculate_output", None),
        )
        self.is_period_size_independent = self.set(
            attr,
            "is_period_size_independent",
            allowed_type=bool,
            default=config.VALUE_TYPES[self.value_type]["is_period_size_independent"],
        )

        self.introspection_data = self.set(
            attr,
            "introspection_data",
        )
        # our custom code
        self.metadata = self.set(attr, 'metadata', allowed_type = dict, setter = self.set_metadata, default = {})

        formulas_attr, unexpected_attrs = helpers._partition(
            attr,
            lambda name, value: name.startswith(config.FORMULA_NAME_PREFIX),
        )
        self.formulas = self.set_formulas(formulas_attr)

        if unexpected_attrs:
            msg = 'Unexpected attributes in definition of variable "{}": {!r}'.format(
                self.name,
                ", ".join(sorted(unexpected_attrs.keys())),
            )
            raise ValueError(
                msg,
            )

        self.is_neutralized = False

    # our custom code
    def set_metadata(self, metadata):
        if metadata:
            return metadata
