import logging
from typing import Any, List, Dict

import polars as pl

from src.models.sink_config import SinkConfig
from src.utils.delta_client import DeltaClient


class Write:
    def __init__(self, sink_config: SinkConfig, delta_client: DeltaClient) -> None:
        self.sink_config = sink_config
        self.delta_client = delta_client

    def execute(self, df: pl.DataFrame) -> None:
        table_uri = f"{self.sink_config.table_base_uri}"
        table_name = self.sink_config.table_name

        if isinstance(df, pl.DataFrame):
            if not df.is_empty():
                logging.info(f"Attempt To Write To Delta Table {table_name}!")
                self.delta_client.write_to_delta(
                    df=df,
                    mode=self.sink_config.mode,
                    table_uri=table_uri,
                    table_name=table_name,
                    overwrite_schema=self.sink_config.overwrite_schema,
                )

                history: List[Dict[str, Any]] = self.delta_client.get_delta_table(
                    table_uri=table_uri,
                    table_name=table_name,
                ).history()

                # To Show Operation Work For Now
                history_df = pl.DataFrame(history).limit(n=10)
                logging.info(f"Delta Table History: {history_df}")

            else:
                logging.warning(
                    f"Will Not Write To Delta Table {table_name}! Input Data Is Empty!"
                )
