import os
import random
import string
import time

import pytest
import requests

from pyatlan.cache.role_cache import RoleCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.error import NotFoundError
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Column,
    Connection,
    Database,
    Schema,
    Table,
    View,
)
from pyatlan.model.core import Announcement
from pyatlan.model.enums import AnnouncementType, AtlanConnectorType

GUIDS_UNABLE_TO_DELETE = {
    "c85a9054-e80d-4e6f-b7d9-5967c39b5868",
    "a6c823a5-51ca-4651-9356-2b4c8bebdf46",
    "13f1e4fa-b7fb-455c-b604-f900c1d202ec",
    "a63db828-cf3b-42b3-a0be-31ce27826c4f",
    "ed165dba-9fc9-466c-8c96-26e1ff2efe13",
    "8fe222aa-93f1-46a3-825c-f85c59079c97",
    "63aa0a7f-bfc0-4ca7-87ed-3d0e9200b9fe",
    "25865e20-cb7d-497b-bf2f-97bcc9f02a96",
    "711b6004-1b84-49fe-ac42-e0d42bfa01fc",
    "34d8106a-1478-4816-bfe1-97814ffff78e",
    "04a4eca5-b7d5-4659-bbad-1dc2306ea9c3",
    "619daa76-ab3c-4f29-836a-6ec0ddefbe0c",
    "4af8d57c-61ef-4b57-983c-eff20e6d08b5",
    "57f5463d-cc2a-4859-bf28-e4fa52002e8e",
}


@pytest.fixture(scope="module")
def client() -> AtlanClient:
    return AtlanClient()


@pytest.fixture()
def announcement() -> Announcement:
    return Announcement(
        announcement_title="Important Announcement",
        announcement_message="A message".join(
            random.choices(string.ascii_lowercase, k=20)  # nosec
        ),
        announcement_type=AnnouncementType.ISSUE,
    )


@pytest.fixture(scope="session")
def atlan_host() -> str:
    return get_environment_variable("ATLAN_HOST")


@pytest.fixture(scope="session")
def atlan_api_key() -> str:
    return get_environment_variable("ATLAN_API_KEY")


@pytest.fixture(scope="session")
def headers(atlan_api_key):
    return {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "authorization": f"Bearer {atlan_api_key}",
    }


def get_environment_variable(name) -> str:
    ret_value = os.environ[name]
    assert ret_value
    return ret_value


@pytest.fixture()
def increment_counter():
    i = random.randint(0, 1000)

    def increment():
        nonlocal i
        i += 1
        return i

    return increment


@pytest.fixture()
def glossary_guids(atlan_host, headers):
    return get_guids(atlan_host, headers, "AtlasGlossary")


@pytest.fixture()
def create_glossary(atlan_host, headers, increment_counter):
    def create_it():
        suffix = increment_counter()
        url = f"{atlan_host}/api/meta/entity/bulk"
        payload = {
            "entities": [
                {
                    "attributes": {
                        "userDescription": f"Integration Test Glossary {suffix}",
                        "name": f"Integration Test Glossary {suffix}",
                        "qualifiedName": "",
                        "certificateStatus": "DRAFT",
                        "ownersUsers": [],
                        "ownerGroups": [],
                    },
                    "typeName": "AtlasGlossary",
                }
            ]
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        guid = list(data["guidAssignments"].values())[0]
        return guid

    return create_it


def get_guids(atlan_host, headers, type_name):
    url = f"{atlan_host}/api/meta/search/indexsearch"

    payload = {
        "dsl": {
            "from": 0,
            "size": 100,
            "query": {
                "bool": {
                    "must": [
                        {"term": {"__state": "ACTIVE"}},
                        {"prefix": {"name.keyword": {"value": "Integration"}}},
                    ]
                }
            },
            "post_filter": {
                "bool": {"filter": {"term": {"__typeName.keyword": type_name}}}
            },
        },
        "attributes": ["connectorName"],
    }

    response = requests.request("POST", url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    if "entities" in data:
        return [entity["guid"] for entity in data["entities"]]
    else:
        return []


def delete_asset(atlan_host, headers, guid):
    url = f"{atlan_host}/api/meta/entity/guid/{guid}?deleteType=HARD"
    response = requests.delete(url, headers=headers)
    return response.status_code


def delete_assets(atlan_host, headers, type_name):
    for guid in get_guids(atlan_host, headers, type_name):
        if delete_asset(atlan_host, headers, guid) != 200:
            print(f"Failed to delete {type_name} with guid {guid}")
            if guid not in GUIDS_UNABLE_TO_DELETE:
                print(f"\t new guid: {guid}")


@pytest.fixture(autouse=True, scope="module")
def cleanup(atlan_host, headers, atlan_api_key):
    type_names = [
        "AtlasGlossaryTerm",
        "AtlasGlossaryCategory",
        "AtlasGlossary",
        "Table",
        "Schema",
        "Database",
        "Connection",
        "View",
    ]
    for type_name in type_names:
        print()
        delete_assets(atlan_host, headers, type_name)
    yield
    for type_name in type_names:
        delete_assets(atlan_host, headers, type_name)


def test_get_glossary_by_guid_good_guid(create_glossary, client: AtlanClient):
    glossary = client.get_asset_by_guid(create_glossary(), AtlasGlossary)
    assert isinstance(glossary, AtlasGlossary)


def test_get_asset_by_guid_when_table_specified_and_glossary_returned_raises_not_found_error(
    create_glossary, client: AtlanClient
):
    with pytest.raises(NotFoundError) as ex_info:
        guid = create_glossary()
        client.get_asset_by_guid(guid, Table)
    assert (
        f"Asset with GUID {guid} is not of the type requested: Table."
        in ex_info.value.args[0]
    )


def test_get_glossary_by_guid_bad_guid(client: AtlanClient):
    with pytest.raises(NotFoundError) as ex_info:
        client.get_asset_by_guid("76d54dd6-925b-499b-a455-6", AtlasGlossary)
    assert (
        "Given instance guid 76d54dd6-925b-499b-a455-6 is invalid/not found"
        in ex_info.value.args[0]
    )


def test_update_glossary_when_no_changes(create_glossary, client: AtlanClient):
    glossary = client.get_asset_by_guid(create_glossary(), AtlasGlossary)
    response = client.upsert(glossary)
    assert not response.guid_assignments
    assert not response.mutated_entities


def test_update_glossary_with_changes(
    create_glossary, client: AtlanClient, announcement
):
    glossary = client.get_asset_by_guid(create_glossary(), AtlasGlossary)
    glossary.set_announcement(announcement)
    response = client.upsert(glossary)
    assert not response.guid_assignments
    assert response.mutated_entities
    assert not response.mutated_entities.CREATE
    assert not response.mutated_entities.DELETE
    assert response.mutated_entities.UPDATE
    assert len(response.mutated_entities.UPDATE) == 1
    assert isinstance(response.mutated_entities.UPDATE[0], AtlasGlossary)
    glossary = response.mutated_entities.UPDATE[0]
    assert glossary.attributes.announcement_title == announcement.announcement_title


def test_purge_glossary(create_glossary, client: AtlanClient):
    response = client.purge_entity_by_guid(create_glossary())
    assert response.mutated_entities
    assert response.mutated_entities.DELETE
    assert len(response.mutated_entities.DELETE) == 1
    assert not response.mutated_entities.UPDATE
    assert not response.mutated_entities.CREATE


def test_create_glossary(client: AtlanClient, increment_counter):
    glossary = AtlasGlossary.create(f"Integration Test Glossary {increment_counter()}")
    response = client.upsert(glossary)
    assert response.mutated_entities
    assert not response.mutated_entities.UPDATE
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    assert response.guid_assignments[glossary.guid]
    guid = response.guid_assignments[glossary.guid]
    assert response.mutated_entities.CREATE
    assert isinstance(response.mutated_entities.CREATE[0], AtlasGlossary)
    glossary = response.mutated_entities.CREATE[0]
    assert glossary.guid == guid


def test_create_multiple_glossaries_one_at_time(client: AtlanClient, increment_counter):
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name=f"Integration Test Glossary {increment_counter()}",
            user_description="This a test glossary",
        )
    )
    response = client.upsert(glossary)
    assert response.mutated_entities
    assert not response.mutated_entities.UPDATE
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[glossary.guid]
    assert isinstance(response.mutated_entities.CREATE[0], AtlasGlossary)
    glossary = response.mutated_entities.CREATE[0]
    assert glossary.guid == guid
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name=f"Integration Test Glossary {increment_counter()}",
            user_description="This a test glossary",
        )
    )
    response = client.upsert(glossary)
    assert response.mutated_entities
    assert not response.mutated_entities.UPDATE
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[glossary.guid]
    assert isinstance(response.mutated_entities.CREATE[0], AtlasGlossary)
    glossary = response.mutated_entities.CREATE[0]
    assert glossary.guid == guid


def test_create_multiple_glossaries(client: AtlanClient, increment_counter):
    entities: list[Asset] = []
    count = 2
    for i in range(count):
        entities.append(
            AtlasGlossary(
                attributes=AtlasGlossary.Attributes(
                    name=f"Integration Test Glossary {increment_counter() + i}",
                    user_description="This a test glossary",
                )
            )
        )
    response = client.upsert(entities)
    assert response.mutated_entities
    assert not response.mutated_entities.UPDATE
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == count
    for i in range(count):
        guid = response.guid_assignments[entities[i].guid]
        glossary = response.mutated_entities.CREATE[i]
        assert glossary.guid == guid


def test_create_glossary_category(client: AtlanClient, increment_counter):
    suffix = increment_counter()
    glossary = AtlasGlossary.create(f"Integration Test Glossary {suffix}")
    glossary.attributes.user_description = "This a test glossary"
    response = client.upsert(glossary)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert isinstance(response.mutated_entities.CREATE[0], AtlasGlossary)
    glossary = response.mutated_entities.CREATE[0]
    category = AtlasGlossaryCategory.create(
        f"Integration Test Glossary Category {suffix}", anchor=glossary
    )
    category.attributes.user_description = "This is a test glossary category"
    response = client.upsert(category)
    assert response.mutated_entities
    assert response.mutated_entities.UPDATE
    assert len(response.mutated_entities.UPDATE) == 1
    assert isinstance(response.mutated_entities.UPDATE[0], AtlasGlossary)
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[category.guid]
    assert isinstance(response.mutated_entities.CREATE[0], AtlasGlossaryCategory)
    category = response.mutated_entities.CREATE[0]
    assert isinstance(category, AtlasGlossaryCategory)
    assert guid == category.guid
    category = client.get_asset_by_guid(guid, AtlasGlossaryCategory)
    assert isinstance(category, AtlasGlossaryCategory)
    assert category.guid == guid


def test_create_glossary_term(client: AtlanClient, increment_counter):
    suffix = increment_counter()
    glossary = AtlasGlossary.create(f"Integration Test Glossary {suffix}")
    response = client.upsert(glossary)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert isinstance(response.mutated_entities.CREATE[0], AtlasGlossary)
    glossary = response.mutated_entities.CREATE[0]
    term = AtlasGlossaryTerm.create(
        f"Integration Test Glossary Term {suffix}", anchor=glossary
    )
    response = client.upsert(term)
    assert response.mutated_entities
    assert response.mutated_entities.UPDATE
    assert response.mutated_entities.UPDATE
    assert len(response.mutated_entities.UPDATE) == 1
    assert isinstance(response.mutated_entities.UPDATE[0], AtlasGlossary)
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    guid = response.guid_assignments[term.guid]
    assert isinstance(response.mutated_entities.CREATE[0], AtlasGlossaryTerm)
    term = response.mutated_entities.CREATE[0]
    assert guid == term.guid
    term = client.get_asset_by_guid(guid, AtlasGlossaryTerm)
    assert isinstance(term, AtlasGlossaryTerm)
    assert term.guid == guid


def test_create_hierarchy(client: AtlanClient, increment_counter):
    suffix = increment_counter()
    glossary = AtlasGlossary(
        attributes=AtlasGlossary.Attributes(
            name=f"Integration Test Glossary {suffix}",
            user_description="This a test glossary",
        )
    )
    response = client.upsert(glossary)
    assert len(response.assets_created(AtlasGlossary)) == 1
    glossary = response.assets_created(AtlasGlossary)[0]
    category_1 = AtlasGlossaryCategory(
        attributes=AtlasGlossaryCategory.Attributes(
            name=f"Integration Test Glossary Category {suffix}",
            user_description="This is a test glossary category",
            anchor=glossary,
        )
    )
    response = client.upsert(category_1)
    assert len(response.assets_updated(AtlasGlossary)) == 1
    assert len(response.assets_created(AtlasGlossaryCategory)) == 1
    guid = response.guid_assignments[category_1.guid]
    category_1 = response.assets_created(AtlasGlossaryCategory)[0]
    assert guid == category_1.guid
    category_2 = AtlasGlossaryCategory.create(
        name=f"Integration Test Glossary Category {suffix}",
        anchor=glossary,
        parent_category=category_1,
    )
    response = client.upsert(category_2)
    guid = response.guid_assignments[category_2.guid]
    assert len(response.assets_updated(AtlasGlossary)) == 1
    assert len(response.assets_updated(AtlasGlossaryCategory)) == 1
    assert len(response.assets_created(AtlasGlossaryCategory)) == 1
    category_2 = response.assets_created(AtlasGlossaryCategory)[0]
    assert guid == category_2.guid
    term = AtlasGlossaryTerm.create(
        name=f"Integration Test term {suffix}", anchor=glossary, categories=[category_2]
    )
    response = client.upsert(term)
    assert len(response.assets_updated(AtlasGlossary)) == 1
    assert len(response.assets_updated(AtlasGlossaryCategory)) == 1
    guid = response.guid_assignments[term.guid]
    assert len(response.assets_created(AtlasGlossaryTerm)) == 1
    term = response.assets_created(AtlasGlossaryTerm)[0]
    assert guid == term.guid


@pytest.mark.skip("Connection creation is still intermittently failing")
def test_create_connection(client: AtlanClient, increment_counter):
    role = RoleCache.get_id_for_name("$admin")
    assert role
    c = Connection.create(
        name=f"Integration {increment_counter()}",
        connector_type=AtlanConnectorType.SNOWFLAKE,
        admin_roles=[role],
        admin_groups=["admin"],
    )
    response = client.upsert(c)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    assert isinstance(response.mutated_entities.CREATE[0], Connection)
    assert response.guid_assignments
    assert c.guid in response.guid_assignments
    guid = response.guid_assignments[c.guid]
    c = response.mutated_entities.CREATE[0]
    assert guid == c.guid
    c = client.get_asset_by_guid(c.guid, Connection)
    assert isinstance(c, Connection)
    assert c.guid == guid


@pytest.mark.skip("Connection creation is still intermittently failing")
def test_create_database(client: AtlanClient, increment_counter):
    role = RoleCache.get_id_for_name("$admin")
    assert role
    suffix = increment_counter()
    connection = Connection.create(
        name=f"Integration {suffix}",
        connector_type=AtlanConnectorType.SNOWFLAKE,
        admin_roles=[role],
        admin_groups=["admin"],
    )
    response = client.upsert(connection)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert isinstance(response.mutated_entities.CREATE[0], Connection)
    connection = response.mutated_entities.CREATE[0]
    connection = client.get_asset_by_guid(connection.guid, Connection)
    database = Database.create(
        name=f"Integration_{suffix}",
        connection_qualified_name=connection.attributes.qualified_name,
    )
    response = client.upsert(database)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    assert isinstance(response.mutated_entities.CREATE[0], Database)
    assert response.guid_assignments
    assert database.guid in response.guid_assignments
    guid = response.guid_assignments[database.guid]
    database = response.mutated_entities.CREATE[0]
    assert guid == database.guid
    database = client.get_asset_by_guid(guid, Database)
    assert isinstance(database, Database)
    assert guid == database.guid


@pytest.mark.skip("Connection creation is still intermittently failing")
def test_create_schema(client: AtlanClient, increment_counter):
    role = RoleCache.get_id_for_name("$admin")
    assert role
    suffix = increment_counter()
    connection = Connection.create(
        name=f"Integration {suffix}",
        connector_type=AtlanConnectorType.SNOWFLAKE,
        admin_roles=[role],
        admin_groups=["admin"],
    )
    response = client.upsert(connection)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert isinstance(response.mutated_entities.CREATE[0], Connection)
    connection = response.mutated_entities.CREATE[0]
    time.sleep(30)
    connection = client.get_asset_by_guid(connection.guid, Connection)
    database = Database.create(
        name=f"Integration_{suffix}",
        connection_qualified_name=connection.attributes.qualified_name,
    )
    response = client.upsert(database)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert isinstance(response.mutated_entities.CREATE[0], Database)
    database = response.mutated_entities.CREATE[0]
    time.sleep(3)
    database = client.get_asset_by_guid(database.guid, Database)
    schema = Schema.create(
        name=f"Integration_{suffix}",
        database_qualified_name=database.attributes.qualified_name,
    )
    response = client.upsert(schema)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    assert isinstance(response.mutated_entities.CREATE[0], Schema)
    assert response.guid_assignments
    assert schema.guid in response.guid_assignments
    guid = response.guid_assignments[schema.guid]
    schema = response.mutated_entities.CREATE[0]
    assert guid == schema.guid
    time.sleep(3)
    schema = client.get_asset_by_guid(guid, Schema)
    assert isinstance(schema, Schema)
    assert guid == schema.guid


@pytest.mark.skip("Connection creation is still intermittently failing")
def test_create_table(client: AtlanClient, increment_counter):
    role = RoleCache.get_id_for_name("$admin")
    assert role
    suffix = increment_counter()
    connection = Connection.create(
        name=f"Integration {suffix}",
        connector_type=AtlanConnectorType.SNOWFLAKE,
        admin_roles=[role],
        admin_groups=["admin"],
    )
    response = client.upsert(connection)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert isinstance(response.mutated_entities.CREATE[0], Connection)
    connection = response.mutated_entities.CREATE[0]
    time.sleep(30)
    connection = client.get_asset_by_guid(connection.guid, Connection)
    database = Database.create(
        name=f"Integration_{suffix}",
        connection_qualified_name=connection.attributes.qualified_name,
    )
    response = client.upsert(database)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert isinstance(response.mutated_entities.CREATE[0], Database)
    database = response.mutated_entities.CREATE[0]
    time.sleep(3)
    database = client.get_asset_by_guid(database.guid, Database)
    schema = Schema.create(
        name=f"Integration_{suffix}",
        database_qualified_name=database.attributes.qualified_name,
    )
    response = client.upsert(schema)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert isinstance(response.mutated_entities.CREATE[0], Schema)
    schema = response.mutated_entities.CREATE[0]
    time.sleep(3)
    schema = client.get_asset_by_guid(schema.guid, Schema)
    table = Table.create(
        name=f"Integration_{suffix}",
        schema_qualified_name=schema.attributes.qualified_name,
    )
    response = client.upsert(table)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    assert isinstance(response.mutated_entities.CREATE[0], Table)
    assert response.guid_assignments
    assert table.guid in response.guid_assignments
    guid = response.guid_assignments[table.guid]
    table = response.mutated_entities.CREATE[0]
    assert guid == table.guid
    time.sleep(3)
    table = client.get_asset_by_guid(guid, Table)
    assert isinstance(table, Table)
    assert guid == table.guid


def test_get_by_qualified_name(client: AtlanClient):
    qualified_name = "default/snowflake/1646836521/ATLAN_SAMPLE_DATA/DBT_SARORA/RAW_CUSTOMERS/LAST_NAME"
    column = client.get_asset_by_qualified_name(
        qualified_name=qualified_name, asset_type=Column
    )
    assert column.attributes.qualified_name == qualified_name


@pytest.mark.skip("Connection creation is still intermittently failing")
def test_create_view(client: AtlanClient, increment_counter):
    view = View.create(
        f"Integration {increment_counter()}",
        schema_qualified_name="default/snowflake/1658945299/ATLAN_SAMPLE_DATA/US_ECONOMIC_DATA",
    )
    response = client.upsert(view)
    assert response.mutated_entities
    assert response.mutated_entities.CREATE
    assert len(response.mutated_entities.CREATE) == 1
    assert isinstance(response.mutated_entities.CREATE[0], View)
    assert response.guid_assignments
    assert view.guid in response.guid_assignments
    guid = response.guid_assignments[view.guid]
    view = response.mutated_entities.CREATE[0]
    assert guid == view.guid
