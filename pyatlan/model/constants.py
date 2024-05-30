# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from typing import Literal

DELETED_ = "(DELETED)"
DELETED_SENTINEL = "DeLeTeD_SeNtIn3l"
DOMAIN_TYPES = Literal["DataDomain", "DataProduct"]
ENTITY_TYPES = Literal["Asset"]
GLOSSARY_TYPES = Literal[
    "AtlasGlossary",
    "AtlasGlossaryCategory",
    "AtlasGlossaryTerm",
]
OTHER_ASSET_TYPES = Literal["File"]
ASSET_TYPES = Literal[
    "ADLSAccount",
    "ADLSContainer",
    "ADLSObject",
    "APIPath",
    "APISpec",
    "Collection",
    "Query",
    "BIProcess",
    "Badge",
    "Column",
    "ColumnProcess",
    "Connection",
    "DataStudioAsset",
    "Database",
    "DbtColumnProcess",
    "DbtMetric",
    "DbtModel",
    "DbtModelColumn",
    "DbtProcess",
    "DbtSource",
    "Folder",
    "GCSBucket",
    "GCSObject",
    "Insight",
    "KafkaConsumerGroup",
    "KafkaTopic",
    "Process",
    "Link",
    "LookerDashboard",
    "LookerExplore",
    "LookerField",
    "LookerFolder",
    "LookerLook",
    "LookerModel",
    "LookerProject",
    "LookerQuery",
    "LookerTile",
    "LookerView",
    "MCIncident",
    "MCMonitor",
    "MaterialisedView",
    "MetabaseCollection",
    "MetabaseDashboard",
    "MetabaseQuestion",
    "ModeChart",
    "ModeCollection",
    "ModeQuery",
    "ModeReport",
    "ModeWorkspace",
    "PowerBIColumn",
    "PowerBIDashboard",
    "PowerBIDataflow",
    "PowerBIDataset",
    "PowerBIDatasource",
    "PowerBIMeasure",
    "PowerBIPage",
    "PowerBIReport",
    "PowerBITable",
    "PowerBITile",
    "PowerBIWorkspace",
    "PresetChart",
    "PresetDashboard",
    "PresetDataset",
    "PresetWorkspace",
    "Procedure",
    "QlikApp",
    "QlikChart",
    "QlikDataset",
    "QlikSheet",
    "QlikSpace",
    "QlikStream",
    "QuickSightAnalysis",
    "QuickSightAnalysisVisual",
    "QuickSightDashboard",
    "QuickSightDashboardVisual",
    "QuickSightDataset",
    "QuickSightDatasetField",
    "QuickSightFolder",
    "Readme",
    "ReadmeTemplate",
    "RedashDashboard",
    "RedashQuery",
    "RedashVisualization",
    "S3Bucket",
    "S3Object",
    "SalesforceDashboard",
    "SalesforceField",
    "SalesforceObject",
    "SalesforceOrganization",
    "SalesforceReport",
    "Schema",
    "SigmaDataElement",
    "SigmaDataElementField",
    "SigmaDataset",
    "SigmaDatasetColumn",
    "SigmaPage",
    "SigmaWorkbook",
    "SnowflakePipe",
    "SnowflakeStream",
    "SnowflakeTag",
    "Table",
    "TablePartition",
    "TableauCalculatedField",
    "TableauDashboard",
    "TableauDatasource",
    "TableauDatasourceField",
    "TableauFlow",
    "TableauMetric",
    "TableauProject",
    "TableauSite",
    "TableauWorkbook",
    "TableauWorksheet",
    "ThoughtspotAnswer",
    "ThoughtspotDashlet",
    "ThoughtspotLiveboard",
    "View",
]
