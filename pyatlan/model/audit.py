from datetime import datetime
from enum import Enum
from typing import Any, Generator, Iterable, Optional, Union

from pydantic import Field, ValidationError, parse_obj_as, root_validator

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.client.constants import AUDIT_SEARCH
from pyatlan.client.workflow import ApiCaller
from pyatlan.errors import ErrorCode, NotFoundError
from pyatlan.model.assets import Asset
from pyatlan.model.core import AtlanObject, AtlanTag
from pyatlan.model.search import (
    DSL,
    Bool,
    Query,
    SearchRequest,
    SortItem,
    SortOrder,
    Term,
)

TOTAL_COUNT = "totalCount"

ENTITY_AUDITS = "entityAudits"

ATTRIBUTES = "attributes"

TYPE_NAME = "type_name"

LATEST_FIRST = [SortItem("created", order=SortOrder.DESCENDING)]


class AuditActionType(str, Enum):
    ENTITY_CREATE = "ENTITY_CREATE"
    ENTITY_UPDATE = "ENTITY_UPDATE"
    ENTITY_DELETE = "ENTITY_DELETE"
    CUSTOM_METADATA_UPDATE = "BUSINESS_ATTRIBUTE_UPDATE"
    ATLAN_TAG_ADD = "CLASSIFICATION_ADD"
    PROPAGATED_ATLAN_TAG_ADD = "PROPAGATED_CLASSIFICATION_ADD"
    ATLAN_TAG_DELETE = "CLASSIFICATION_DELETE"
    PROPAGATED_ATLAN_TAG_DELETE = "PROPAGATED_CLASSIFICATION_DELETE"
    ENTITY_IMPORT_CREATE = "ENTITY_IMPORT_CREATE"
    ENTITY_IMPORT_UPDATE = "ENTITY_IMPORT_UPDATE"
    ENTITY_IMPORT_DELETE = "ENTITY_IMPORT_DELETE"
    ATLAN_TAG_UPDATE = "CLASSIFICATION_UPDATE"
    PROPAGATED_ATLAN_TAG_UPDATE = "PROPAGATED_CLASSIFICATION_UPDATE"
    TERM_ADD = "TERM_ADD"
    TERM_DELETE = "TERM_DELETE"


class AuditSearchRequest(SearchRequest):
    """Class from which to configure a search against Atlan's activity log."""

    dsl: DSL
    attributes: list[str] = Field(default_factory=list, alias="attributes")

    class Config:
        json_encoders = {Query: lambda v: v.to_dict(), SortItem: lambda v: v.to_dict()}

    @classmethod
    def by_guid(
        cls, guid: str, *, size: int = 10, _from: int = 0
    ) -> "AuditSearchRequest":
        """
        Create an audit search request for the last changes to an asset, by its GUID.
        :param guid: unique identifier of the asset for which to retrieve the audit history
        :param size: number of changes to retrieve
        :param _from: starting point for paging. Defaults to 0 (very first result) if not overridden
        :returns: an AuditSearchRequest that can be used to perform the search
        """
        dsl = DSL(
            query=Bool(filter=[Term(field="entityId", value=guid)]),
            sort=LATEST_FIRST,
            size=size,
            _from=_from,
        )
        return AuditSearchRequest(dsl=dsl)

    @classmethod
    def by_user(
        cls, user: str, *, size: int = 10, _from: int = 0
    ) -> "AuditSearchRequest":
        """
        Create an audit search request for the last changes to an asset, by a given user.
        :param user: the name of the user for which to look for any changes
        :param size: number of changes to retrieve
        :param _from: starting point for paging. Defaults to 0 (very first result) if not overridden
        :returns: an AuditSearchRequest that can be used to perform the search
        """
        dsl = DSL(
            query=Bool(filter=[Term(field="user", value=user)]),
            sort=LATEST_FIRST,
            size=size,
            _from=_from,
        )
        return AuditSearchRequest(dsl=dsl)

    @classmethod
    def by_qualified_name(
        cls, type_name: str, qualified_name: str, *, size: int = 10, _from: int = 0
    ) -> "AuditSearchRequest":
        """
        Create an audit search request ffor the last changes to an asset, by its qualifiedName.
        :param type_name: the type of asset for which to retrieve the audit history
        :param qualified_name: unique name of the asset for which to retrieve the audit history
        :param size: number of changes to retrieve
        :param _from: starting point for paging. Defaults to 0 (very first result) if not overridden
        :returns: an AuditSearchRequest that can be used to perform the search
        """
        dsl = DSL(
            query=Bool(
                must=[
                    Term(field="entityQualifiedName", value=qualified_name),
                    Term(field="typeName", value=type_name),
                ]
            ),
            sort=LATEST_FIRST,
            size=size,
            _from=_from,
        )
        return AuditSearchRequest(dsl=dsl)


class CustomMetadataAttributesAuditDetail(AtlanObject):
    """Capture the attributes and values for custom metadata as tracked through the audit log."""

    class Config:
        extra = "forbid"

    type_name: str

    attributes: dict[str, Any]

    archived_attributes: Optional[dict[str, Any]]

    @property
    def empty(self) -> bool:
        return self.attributes is None or len(self.attributes) == 0

    @root_validator()
    def convert(cls, values):
        cm_id = values[TYPE_NAME]
        try:
            values[TYPE_NAME] = CustomMetadataCache.get_name_for_id(values[TYPE_NAME])
            attributes = {
                CustomMetadataCache.get_attr_name_for_id(cm_id, attr_id): properties
                for attr_id, properties in values[ATTRIBUTES].items()
            }
            archived_attributes = {
                key: value for key, value in attributes.items() if "-archived-" in key
            }
            for key in archived_attributes:
                del attributes[key]
            values[ATTRIBUTES] = attributes
            values["archived_attributes"] = archived_attributes
        except NotFoundError:
            values[TYPE_NAME] = "(DELETED)"
            values[ATTRIBUTES] = {}
        return values


class EntityAudit(AtlanObject):
    """
    Detailed entry in the audit log. These objects should be treated as immutable.
    """

    entity_qualified_name: str
    type_name: str
    entity_id: str
    timestamp: datetime
    created: datetime
    user: str
    action: AuditActionType
    details: Optional[Any]
    event_key: str
    entity: Optional[Any]
    type: Optional[Any]
    detail: Optional[Union[CustomMetadataAttributesAuditDetail, AtlanTag, Asset]]
    entity_detail: Optional[Asset]
    headers: Optional[dict[str, str]]


class AuditSearchResults(Iterable):
    """Captures the response from a search against Atlan's activity log."""

    def __init__(
        self,
        client: ApiCaller,
        criteria: AuditSearchRequest,
        start: int,
        size: int,
        entity_audits: list[EntityAudit],
        count: int,
        aggregations: Optional[Any],
    ):
        self._client = client
        self._endpoint = AUDIT_SEARCH
        self._criteria = criteria
        self._start = start
        self._size = size
        self._entity_audits = entity_audits
        self._count = count

    @property
    def total_count(self) -> int:
        return self._count

    def current_page(self) -> list[EntityAudit]:
        """
        Retrieve the current page of results.

        :returns: list of assets on the current page of results
        """
        return self._entity_audits

    def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results.

        :returns: True if there is a next page of results, otherwise False
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._entity_audits else False

    def _get_next_page(self):
        """
        Fetches the next page of results.

        :returns: True if the next page of results was fetched, False if there was no next page
        """
        self._criteria.dsl.from_ = self._start
        self._criteria.dsl.size = self._size
        if raw_json := self._get_next_page_json():
            self._count = raw_json[TOTAL_COUNT] if TOTAL_COUNT in raw_json else 0
            return True
        return False

    def _get_next_page_json(self):
        """
        Fetches the next page of results and returns the raw JSON of the retrieval.

        :returns: JSON for the next page of results, as-is
        """
        raw_json = self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if ENTITY_AUDITS not in raw_json or not raw_json[ENTITY_AUDITS]:
            self._entity_audits = []
            return None
        try:
            self._assets = parse_obj_as(list[EntityAudit], raw_json[ENTITY_AUDITS])
            return raw_json
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    def __iter__(self) -> Generator[EntityAudit, None, None]:
        """
        Iterates through the results, lazily-fetching each next page until there
        are no more results.

        :returns: an iterable form of each result, across all pages
        """
        while True:
            yield from self.current_page()
            if not self.next_page():
                break
