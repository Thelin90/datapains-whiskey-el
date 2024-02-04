from dataclasses import dataclass
from typing import Any, Dict

from src.models.api_config import ApiConfig
from src.models.base_config import BaseConfig
from src.models.sink_config import SinkConfig


@dataclass(frozen=False)
class ApplicationConfig:
    base_config: BaseConfig
    api_config: ApiConfig
    sink_config: SinkConfig


@dataclass(frozen=False)
class Config:
    config: Dict[str, Dict[str, Any]]

    def set_application_config(self) -> ApplicationConfig:
        base_config = BaseConfig(**self.config["base"])
        api_config = ApiConfig(**self.config["api"])
        sink_config = SinkConfig(**self.config["sink"])

        if base_config is not None and api_config is not None:
            return ApplicationConfig(
                base_config=base_config, api_config=api_config, sink_config=sink_config
            )
        else:
            raise ValueError("Not all configuration set!")
