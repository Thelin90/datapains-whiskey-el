from dataclasses import dataclass


@dataclass(frozen=False)
class SinkConfig:
    mode: str
    hwm: bool
    endpoint_url: str
    table_name: str
    table_base_uri: str
    date_hwm_compare: str
    overwrite_schema: bool
