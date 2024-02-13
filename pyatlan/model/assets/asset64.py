# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .asset37 import GCS


class GCSObject(GCS):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(cls, *, name: str, gcs_bucket_qualified_name: str) -> GCSObject:
        validate_required_fields(
            ["name", "gcs_bucket_qualified_name"], [name, gcs_bucket_qualified_name]
        )
        attributes = GCSObject.Attributes.create(
            name=name, gcs_bucket_qualified_name=gcs_bucket_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="GCSObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCSObject":
            raise ValueError("must be GCSObject")
        return v

    def __setattr__(self, name, value):
        if name in GCSObject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    GCS_BUCKET_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "gcsBucketName", "gcsBucketName.keyword", "gcsBucketName"
    )
    """
    Simple name of the bucket in which this object exists.
    """
    GCS_BUCKET_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "gcsBucketQualifiedName",
        "gcsBucketQualifiedName",
        "gcsBucketQualifiedName.text",
    )
    """
    Unique name of the bucket in which this object exists.
    """
    GCS_OBJECT_SIZE: ClassVar[NumericField] = NumericField(
        "gcsObjectSize", "gcsObjectSize"
    )
    """
    Object size in bytes.
    """
    GCS_OBJECT_KEY: ClassVar[KeywordTextField] = KeywordTextField(
        "gcsObjectKey", "gcsObjectKey", "gcsObjectKey.text"
    )
    """
    Key of this object, in GCS.
    """
    GCS_OBJECT_MEDIA_LINK: ClassVar[KeywordTextField] = KeywordTextField(
        "gcsObjectMediaLink", "gcsObjectMediaLink", "gcsObjectMediaLink.text"
    )
    """
    Media link to this object.
    """
    GCS_OBJECT_HOLD_TYPE: ClassVar[KeywordField] = KeywordField(
        "gcsObjectHoldType", "gcsObjectHoldType"
    )
    """
    Type of hold on this object.
    """
    GCS_OBJECT_GENERATION_ID: ClassVar[NumericField] = NumericField(
        "gcsObjectGenerationId", "gcsObjectGenerationId"
    )
    """
    Generation ID of this object.
    """
    GCS_OBJECT_CRC32C_HASH: ClassVar[KeywordField] = KeywordField(
        "gcsObjectCRC32CHash", "gcsObjectCRC32CHash"
    )
    """
    CRC32C hash of this object.
    """
    GCS_OBJECT_MD5HASH: ClassVar[KeywordField] = KeywordField(
        "gcsObjectMD5Hash", "gcsObjectMD5Hash"
    )
    """
    MD5 hash of this object.
    """
    GCS_OBJECT_DATA_LAST_MODIFIED_TIME: ClassVar[NumericField] = NumericField(
        "gcsObjectDataLastModifiedTime", "gcsObjectDataLastModifiedTime"
    )
    """
    Time (epoch) at which this object's data was last modified, in milliseconds.
    """
    GCS_OBJECT_CONTENT_TYPE: ClassVar[KeywordField] = KeywordField(
        "gcsObjectContentType", "gcsObjectContentType"
    )
    """
    Type of content in this object.
    """
    GCS_OBJECT_CONTENT_ENCODING: ClassVar[KeywordField] = KeywordField(
        "gcsObjectContentEncoding", "gcsObjectContentEncoding"
    )
    """
    Content encoding of this object.
    """
    GCS_OBJECT_CONTENT_DISPOSITION: ClassVar[KeywordField] = KeywordField(
        "gcsObjectContentDisposition", "gcsObjectContentDisposition"
    )
    """
    Information about how this object's content should be presented.
    """
    GCS_OBJECT_CONTENT_LANGUAGE: ClassVar[KeywordField] = KeywordField(
        "gcsObjectContentLanguage", "gcsObjectContentLanguage"
    )
    """
    Language of this object's contents.
    """
    GCS_OBJECT_RETENTION_EXPIRATION_DATE: ClassVar[NumericField] = NumericField(
        "gcsObjectRetentionExpirationDate", "gcsObjectRetentionExpirationDate"
    )
    """
    Retention expiration date of this object.
    """

    GCS_BUCKET: ClassVar[RelationField] = RelationField("gcsBucket")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "gcs_bucket_name",
        "gcs_bucket_qualified_name",
        "gcs_object_size",
        "gcs_object_key",
        "gcs_object_media_link",
        "gcs_object_hold_type",
        "gcs_object_generation_id",
        "gcs_object_c_r_c32_c_hash",
        "gcs_object_m_d5_hash",
        "gcs_object_data_last_modified_time",
        "gcs_object_content_type",
        "gcs_object_content_encoding",
        "gcs_object_content_disposition",
        "gcs_object_content_language",
        "gcs_object_retention_expiration_date",
        "gcs_bucket",
    ]

    @property
    def gcs_bucket_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_bucket_name

    @gcs_bucket_name.setter
    def gcs_bucket_name(self, gcs_bucket_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_name = gcs_bucket_name

    @property
    def gcs_bucket_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_qualified_name
        )

    @gcs_bucket_qualified_name.setter
    def gcs_bucket_qualified_name(self, gcs_bucket_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_qualified_name = gcs_bucket_qualified_name

    @property
    def gcs_object_size(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.gcs_object_size

    @gcs_object_size.setter
    def gcs_object_size(self, gcs_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_size = gcs_object_size

    @property
    def gcs_object_key(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_object_key

    @gcs_object_key.setter
    def gcs_object_key(self, gcs_object_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_key = gcs_object_key

    @property
    def gcs_object_media_link(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.gcs_object_media_link
        )

    @gcs_object_media_link.setter
    def gcs_object_media_link(self, gcs_object_media_link: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_media_link = gcs_object_media_link

    @property
    def gcs_object_hold_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_object_hold_type

    @gcs_object_hold_type.setter
    def gcs_object_hold_type(self, gcs_object_hold_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_hold_type = gcs_object_hold_type

    @property
    def gcs_object_generation_id(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_generation_id
        )

    @gcs_object_generation_id.setter
    def gcs_object_generation_id(self, gcs_object_generation_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_generation_id = gcs_object_generation_id

    @property
    def gcs_object_c_r_c32_c_hash(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_c_r_c32_c_hash
        )

    @gcs_object_c_r_c32_c_hash.setter
    def gcs_object_c_r_c32_c_hash(self, gcs_object_c_r_c32_c_hash: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_c_r_c32_c_hash = gcs_object_c_r_c32_c_hash

    @property
    def gcs_object_m_d5_hash(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_object_m_d5_hash

    @gcs_object_m_d5_hash.setter
    def gcs_object_m_d5_hash(self, gcs_object_m_d5_hash: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_m_d5_hash = gcs_object_m_d5_hash

    @property
    def gcs_object_data_last_modified_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_data_last_modified_time
        )

    @gcs_object_data_last_modified_time.setter
    def gcs_object_data_last_modified_time(
        self, gcs_object_data_last_modified_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_data_last_modified_time = (
            gcs_object_data_last_modified_time
        )

    @property
    def gcs_object_content_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.gcs_object_content_type
        )

    @gcs_object_content_type.setter
    def gcs_object_content_type(self, gcs_object_content_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_type = gcs_object_content_type

    @property
    def gcs_object_content_encoding(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_content_encoding
        )

    @gcs_object_content_encoding.setter
    def gcs_object_content_encoding(self, gcs_object_content_encoding: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_encoding = gcs_object_content_encoding

    @property
    def gcs_object_content_disposition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_content_disposition
        )

    @gcs_object_content_disposition.setter
    def gcs_object_content_disposition(
        self, gcs_object_content_disposition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_disposition = gcs_object_content_disposition

    @property
    def gcs_object_content_language(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_content_language
        )

    @gcs_object_content_language.setter
    def gcs_object_content_language(self, gcs_object_content_language: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_content_language = gcs_object_content_language

    @property
    def gcs_object_retention_expiration_date(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_object_retention_expiration_date
        )

    @gcs_object_retention_expiration_date.setter
    def gcs_object_retention_expiration_date(
        self, gcs_object_retention_expiration_date: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_retention_expiration_date = (
            gcs_object_retention_expiration_date
        )

    @property
    def gcs_bucket(self) -> Optional[GCSBucket]:
        return None if self.attributes is None else self.attributes.gcs_bucket

    @gcs_bucket.setter
    def gcs_bucket(self, gcs_bucket: Optional[GCSBucket]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket = gcs_bucket

    class Attributes(GCS.Attributes):
        gcs_bucket_name: Optional[str] = Field(default=None, description="")
        gcs_bucket_qualified_name: Optional[str] = Field(default=None, description="")
        gcs_object_size: Optional[int] = Field(default=None, description="")
        gcs_object_key: Optional[str] = Field(default=None, description="")
        gcs_object_media_link: Optional[str] = Field(default=None, description="")
        gcs_object_hold_type: Optional[str] = Field(default=None, description="")
        gcs_object_generation_id: Optional[int] = Field(default=None, description="")
        gcs_object_c_r_c32_c_hash: Optional[str] = Field(default=None, description="")
        gcs_object_m_d5_hash: Optional[str] = Field(default=None, description="")
        gcs_object_data_last_modified_time: Optional[datetime] = Field(
            default=None, description=""
        )
        gcs_object_content_type: Optional[str] = Field(default=None, description="")
        gcs_object_content_encoding: Optional[str] = Field(default=None, description="")
        gcs_object_content_disposition: Optional[str] = Field(
            default=None, description=""
        )
        gcs_object_content_language: Optional[str] = Field(default=None, description="")
        gcs_object_retention_expiration_date: Optional[datetime] = Field(
            default=None, description=""
        )
        gcs_bucket: Optional[GCSBucket] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, name: str, gcs_bucket_qualified_name: str
        ) -> GCSObject.Attributes:
            validate_required_fields(
                ["name", "gcs_bucket_qualified_name"], [name, gcs_bucket_qualified_name]
            )

            # Split the gcs_bucket_qualified_name to extract necessary information
            fields = gcs_bucket_qualified_name.split("/")
            if len(fields) != 4:
                raise ValueError("Invalid gcs_bucket_qualified_name")

            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid gcs_bucket_qualified_name") from e

            return GCSObject.Attributes(
                name=name,
                gcs_bucket_qualified_name=gcs_bucket_qualified_name,
                connection_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}",
                qualified_name=f"{gcs_bucket_qualified_name}/{name}",
                connector_name=connector_type.value,
                gcs_bucket=GCSBucket.ref_by_qualified_name(gcs_bucket_qualified_name),
            )

    attributes: "GCSObject.Attributes" = Field(
        default_factory=lambda: GCSObject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class GCSBucket(GCS):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(cls, *, name: str, connection_qualified_name: str) -> GCSBucket:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = GCSBucket.Attributes.create(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="GCSBucket", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCSBucket":
            raise ValueError("must be GCSBucket")
        return v

    def __setattr__(self, name, value):
        if name in GCSBucket._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    GCS_OBJECT_COUNT: ClassVar[NumericField] = NumericField(
        "gcsObjectCount", "gcsObjectCount"
    )
    """
    Number of objects within the bucket.
    """
    GCS_BUCKET_VERSIONING_ENABLED: ClassVar[BooleanField] = BooleanField(
        "gcsBucketVersioningEnabled", "gcsBucketVersioningEnabled"
    )
    """
    Whether versioning is enabled on the bucket (true) or not (false).
    """
    GCS_BUCKET_RETENTION_LOCKED: ClassVar[BooleanField] = BooleanField(
        "gcsBucketRetentionLocked", "gcsBucketRetentionLocked"
    )
    """
    Whether retention is locked for this bucket (true) or not (false).
    """
    GCS_BUCKET_RETENTION_PERIOD: ClassVar[NumericField] = NumericField(
        "gcsBucketRetentionPeriod", "gcsBucketRetentionPeriod"
    )
    """
    Retention period for objects in this bucket.
    """
    GCS_BUCKET_RETENTION_EFFECTIVE_TIME: ClassVar[NumericField] = NumericField(
        "gcsBucketRetentionEffectiveTime", "gcsBucketRetentionEffectiveTime"
    )
    """
    Effective time for retention of objects in this bucket.
    """
    GCS_BUCKET_LIFECYCLE_RULES: ClassVar[TextField] = TextField(
        "gcsBucketLifecycleRules", "gcsBucketLifecycleRules"
    )
    """
    Lifecycle rules for this bucket.
    """
    GCS_BUCKET_RETENTION_POLICY: ClassVar[TextField] = TextField(
        "gcsBucketRetentionPolicy", "gcsBucketRetentionPolicy"
    )
    """
    Retention policy for this bucket.
    """

    GCS_OBJECTS: ClassVar[RelationField] = RelationField("gcsObjects")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "gcs_object_count",
        "gcs_bucket_versioning_enabled",
        "gcs_bucket_retention_locked",
        "gcs_bucket_retention_period",
        "gcs_bucket_retention_effective_time",
        "gcs_bucket_lifecycle_rules",
        "gcs_bucket_retention_policy",
        "gcs_objects",
    ]

    @property
    def gcs_object_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.gcs_object_count

    @gcs_object_count.setter
    def gcs_object_count(self, gcs_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_object_count = gcs_object_count

    @property
    def gcs_bucket_versioning_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_versioning_enabled
        )

    @gcs_bucket_versioning_enabled.setter
    def gcs_bucket_versioning_enabled(
        self, gcs_bucket_versioning_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_versioning_enabled = gcs_bucket_versioning_enabled

    @property
    def gcs_bucket_retention_locked(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_locked
        )

    @gcs_bucket_retention_locked.setter
    def gcs_bucket_retention_locked(self, gcs_bucket_retention_locked: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_locked = gcs_bucket_retention_locked

    @property
    def gcs_bucket_retention_period(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_period
        )

    @gcs_bucket_retention_period.setter
    def gcs_bucket_retention_period(self, gcs_bucket_retention_period: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_period = gcs_bucket_retention_period

    @property
    def gcs_bucket_retention_effective_time(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_effective_time
        )

    @gcs_bucket_retention_effective_time.setter
    def gcs_bucket_retention_effective_time(
        self, gcs_bucket_retention_effective_time: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_effective_time = (
            gcs_bucket_retention_effective_time
        )

    @property
    def gcs_bucket_lifecycle_rules(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_lifecycle_rules
        )

    @gcs_bucket_lifecycle_rules.setter
    def gcs_bucket_lifecycle_rules(self, gcs_bucket_lifecycle_rules: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_lifecycle_rules = gcs_bucket_lifecycle_rules

    @property
    def gcs_bucket_retention_policy(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.gcs_bucket_retention_policy
        )

    @gcs_bucket_retention_policy.setter
    def gcs_bucket_retention_policy(self, gcs_bucket_retention_policy: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_bucket_retention_policy = gcs_bucket_retention_policy

    @property
    def gcs_objects(self) -> Optional[list[GCSObject]]:
        return None if self.attributes is None else self.attributes.gcs_objects

    @gcs_objects.setter
    def gcs_objects(self, gcs_objects: Optional[list[GCSObject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_objects = gcs_objects

    class Attributes(GCS.Attributes):
        gcs_object_count: Optional[int] = Field(default=None, description="")
        gcs_bucket_versioning_enabled: Optional[bool] = Field(
            default=None, description=""
        )
        gcs_bucket_retention_locked: Optional[bool] = Field(
            default=None, description=""
        )
        gcs_bucket_retention_period: Optional[int] = Field(default=None, description="")
        gcs_bucket_retention_effective_time: Optional[datetime] = Field(
            default=None, description=""
        )
        gcs_bucket_lifecycle_rules: Optional[str] = Field(default=None, description="")
        gcs_bucket_retention_policy: Optional[str] = Field(default=None, description="")
        gcs_objects: Optional[list[GCSObject]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls, *, name: str, connection_qualified_name: str
        ) -> GCSBucket.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )

            # Split the connection_qualified_name to extract necessary information
            fields = connection_qualified_name.split("/")
            if len(fields) != 3:
                raise ValueError("Invalid connection_qualified_name")

            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid connection_qualified_name") from e

            return GCSBucket.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=connector_type.value,
            )

    attributes: "GCSBucket.Attributes" = Field(
        default_factory=lambda: GCSBucket.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


GCSObject.Attributes.update_forward_refs()


GCSBucket.Attributes.update_forward_refs()
