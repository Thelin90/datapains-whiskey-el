from dataclasses import dataclass


@dataclass(frozen=False)
class BaseConfig:
    log_level: str
