from dataclasses import dataclass


@dataclass(frozen=False)
class SinkConfig:
    mode: str
    table_name: str
    table_base_uri: str
    overwrite_schema: bool
