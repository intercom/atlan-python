DEFAULT = "default"
CONNECTOR_TYPE = "snowflake"
TIME_STAMP = "1686532494"
CONNECTION_NAME = "MyConnection"
DATABASE_NAME = "MyDB"
SCHEMA_NAME = "MySchema"
TABLE_NAME = "MyTable"
VIEW_NAME = "MyView"
COLUMN_NAME = "MyColumn"
GLOSSARY_NAME = "MyGlossary"
GLOSSARY_TERM_NAME = "MyTerm"
GLOSSARY_CATEGORY_NAME = "MyCategory"
AWS_ARN = "arn:aws:s3:::dev-atlan-sources/sample-data/wwi/STOCK_ITEMS/"
BUCKET_NAME = "bucket_123"
S3_OBJECT_NAME = "object"
S3_CONNECTION_QUALIFIED_NAME = "default/s3/1686535364"
S3_OBJECT_QUALIFIED_NAME = f"{S3_CONNECTION_QUALIFIED_NAME}/{AWS_ARN}"
BUCKET_QUALIFIED_NAME = f"{S3_CONNECTION_QUALIFIED_NAME}/{AWS_ARN}"
GLOSSARY_QUALIFIED_NAME = "OpU9a9kG825gAqpamXugf"
GLOSSARY_TERM_QUALIFIED_NAME = "0KVjsIaDcseinHYE7Nq0w@OpU9a9kG825gAqpamXugf"
GLOSSARY_CATEGORY_QUALIFIED_NAME = "1KsdsIaDcseinHYE7Nq0w@OpU9a9kG825gAqpamXugf"
CONNECTION_QUALIFIED_NAME = f"{DEFAULT}/{CONNECTOR_TYPE}/{TIME_STAMP}"
DATABASE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{DATABASE_NAME}"
SCHEMA_QUALIFIED_NAME = f"{DATABASE_QUALIFIED_NAME}/{SCHEMA_NAME}"
TABLE_QUALIFIED_NAME = f"{SCHEMA_QUALIFIED_NAME}/{TABLE_NAME}"
VIEW_QUALIFIED_NAME = f"{SCHEMA_QUALIFIED_NAME}/{VIEW_NAME}"
TABLE_COLUMN_QUALIFIED_NAME = f"{TABLE_QUALIFIED_NAME}/{COLUMN_NAME}"
VIEW_COLUMN_QUALIFIED_NAME = f"{VIEW_QUALIFIED_NAME}/{COLUMN_NAME}"
FILE_NAME = "file.pdf"
FILE_CONNECTION_QUALIFIED_NAME = "default/api/1686535364"
FILE_QUALIFIED_NAME = f"{FILE_CONNECTION_QUALIFIED_NAME}/{FILE_NAME}"
ADLS_ACCOUNT_NAME = "myaccount"
ADLS_CONNECTION_QUALIFIED_NAME = "default/adls/1686535364"
ADLS_QUALIFIED_NAME = f"{ADLS_CONNECTION_QUALIFIED_NAME}/{ADLS_ACCOUNT_NAME}"  # "default/adls/123456789/myaccount"
ADLS_CONNECTOR_TYPE = "adls"
ADLS_CONTAINER_NAME = "mycontainer"
ADLS_OBJECT_NAME = "myobject.csv"
ADLS_ACCOUNT_QUALIFIED_NAME = (
    f"{ADLS_QUALIFIED_NAME}"  # "default/adls/123456789/myaccount"
)
# "default/adls/123456789/myaccount/mycontainer"
ADLS_CONTAINER_QUALIFIED_NAME = f"{ADLS_QUALIFIED_NAME}/{ADLS_CONTAINER_NAME}"
# "default/adls/123456789/myaccount/mycontainer/myobject.csv"
ADLS_OBJECT_QUALIFIED_NAME = f"{ADLS_CONTAINER_QUALIFIED_NAME}/{ADLS_OBJECT_NAME}"
API_SPEC_NAME = "api-spec"
API_PATH_NAME = "/api/path"
API_CONNECTION_QUALIFIED_NAME = "default/api/123456789"
API_QUALIFIED_NAME = f"{API_CONNECTION_QUALIFIED_NAME}/{API_SPEC_NAME}"
API_CONNECTOR_TYPE = "api"
API_PATH_RAW_URI = "/api/path"
API_SPEC_QUALIFIED_NAME = "default/api/123456789/api-spec"
API_PATH_QUALIFIED_NAME = "default/api/123456789/api-spec/api/path"
GCS_BUCKET_NAME = "mybucket"
GCS_CONNECTION_QUALIFIED_NAME = "default/gcs/123456789"
GCS_QUALIFIED_NAME = f"{GCS_CONNECTION_QUALIFIED_NAME}/{GCS_BUCKET_NAME}"
GCS_CONNECTOR_TYPE = "gcs"
GCS_OBJECT_NAME = "myobject.csv"
GCS_BUCKET_QUALIFIED_NAME = f"{GCS_QUALIFIED_NAME}"
GCS_OBJECT_QUALIFIED_NAME = f"{GCS_QUALIFIED_NAME}/{GCS_OBJECT_NAME}"
REPORT_NAME = "gds-report"
SOURCE_NAME = "gds-source"
DATASTUDIO_CONNECTION_QUALIFIED_NAME = "default/datastudio/123456789"
QUALIFIED_NAME_REPORT = f"{DATASTUDIO_CONNECTION_QUALIFIED_NAME}/{REPORT_NAME}"
QUALIFIED_NAME_SOURCE = f"{DATASTUDIO_CONNECTION_QUALIFIED_NAME}/{SOURCE_NAME}"
CONNECTOR_NAME = "datastudio"
PRESET_WORKSPACE_NAME = "ps-workspace"
PRESET_CONNECTION_QUALIFIED_NAME = "default/preset/123456789"
PRESET_WORKSPACE_QUALIFIED_NAME = (
    f"{PRESET_CONNECTION_QUALIFIED_NAME}/{PRESET_WORKSPACE_NAME}"
)
PRESET_CONNECTOR_TYPE = "preset"
PRESET_DASHBOARD_NAME = "ps-collection"
PRESET_DASHBOARD_QUALIFIED_NAME = f"{PRESET_CONNECTION_QUALIFIED_NAME}/{PRESET_WORKSPACE_NAME}/{PRESET_DASHBOARD_NAME}"
PRESET_CHART_NAME = "ps-chart"
PRESET_CHART_QUALIFIED_NAME = f"{PRESET_DASHBOARD_QUALIFIED_NAME}/{PRESET_CHART_NAME}"
PRESET_DATASET_NAME = "ps-dataset"
PRESET_DATASET_QUALIFIED_NAME = (
    f"{PRESET_DASHBOARD_QUALIFIED_NAME}/{PRESET_DATASET_NAME}"
)
DATA_DOMAIN_MESH_SLUG = "dataDomain"
DATA_DOMAIN_MESH_ABBREVIATION = "dataDomain"
DATA_DOMAIN_NAME = "data-domain"
DATA_SUB_DOMAIN_NAME = "data-sub-domain"
DATA_DOMAIN_QUALIFIED_NAME = f"default/domain/{DATA_DOMAIN_MESH_SLUG}"
DATA_PRODUCT_MESH_SLUG = "dataProduct"
DATA_PRODUCT_MESH_ABBREVIATION = "dataProduct"
DATA_PRODUCT_NAME = "data-product"
DATA_PRODUCT_QUALIFIED_NAME = f"default/product/{DATA_PRODUCT_MESH_SLUG}"
