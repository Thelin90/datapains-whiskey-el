from dataclasses import dataclass


@dataclass(frozen=False)
class ApiConfig:
    url: str
    output: str
    parse_date_column: str
