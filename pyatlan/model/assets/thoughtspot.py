# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, TextField

from .b_i import BI


class Thoughtspot(BI):
    """Description"""

    type_name: str = Field(default="Thoughtspot", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Thoughtspot":
            raise ValueError("must be Thoughtspot")
        return v

    def __setattr__(self, name, value):
        if name in Thoughtspot._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    THOUGHTSPOT_CHART_TYPE: ClassVar[KeywordField] = KeywordField(
        "thoughtspotChartType", "thoughtspotChartType"
    )
    """

    """
    THOUGHTSPOT_QUESTION_TEXT: ClassVar[TextField] = TextField(
        "thoughtspotQuestionText", "thoughtspotQuestionText"
    )
    """

    """

    _convenience_properties: ClassVar[List[str]] = [
        "thoughtspot_chart_type",
        "thoughtspot_question_text",
    ]

    @property
    def thoughtspot_chart_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.thoughtspot_chart_type
        )

    @thoughtspot_chart_type.setter
    def thoughtspot_chart_type(self, thoughtspot_chart_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_chart_type = thoughtspot_chart_type

    @property
    def thoughtspot_question_text(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.thoughtspot_question_text
        )

    @thoughtspot_question_text.setter
    def thoughtspot_question_text(self, thoughtspot_question_text: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.thoughtspot_question_text = thoughtspot_question_text

    class Attributes(BI.Attributes):
        thoughtspot_chart_type: Optional[str] = Field(default=None, description="")
        thoughtspot_question_text: Optional[str] = Field(default=None, description="")

    attributes: "Thoughtspot.Attributes" = Field(
        default_factory=lambda: Thoughtspot.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )