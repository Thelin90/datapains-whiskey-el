from typing import Dict, Optional
import logging
from deltalake import write_deltalake
from deltalake import DeltaTable
from deltalake._internal import TableNotFoundError
from deltalake.exceptions import DeltaError
import polars as pl
import os

from src.models.sink_config import SinkConfig


class DeltaWriteError(DeltaError):
    pass


class Write:
    def __init__(self, sink_config: SinkConfig) -> None:
        self.sink_config = sink_config
        self.storage_options = self._setup_storage_options(
            endpoint_url=self.sink_config.endpoint_url,
        )

    @staticmethod
    def _setup_storage_options(endpoint_url: str) -> Dict[str, str]:
        try:
            os.environ["AWS_S3_ALLOW_UNSAFE_RENAME"] = "true"
            os.environ["AWS_STORAGE_ALLOW_HTTP"] = "1"
            os.environ["AWS_ALLOW_HTTP"] = "true"

            return {
                "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SECRET_ACCESS_KEY"],
                "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"],
                "AWS_REGION": os.environ["AWS_REGION"],
                "AWS_ENDPOINT_URL": endpoint_url,
            }
        except KeyError as key_error:
            raise key_error

    def _get_delta(self, table_uri: str, table_name: str) -> Optional[DeltaTable]:
        try:
            table_uri = f"{table_uri}/{table_name}"
            delta_table = DeltaTable(
                storage_options=self.storage_options,
                table_uri=table_uri,
            )

            return delta_table

        except TableNotFoundError as table_not_found_error:
            logging.debug(f"_get_delta: {table_not_found_error}")
            return None

    def _filter_hwm(
        self,
        df: pl.DataFrame,
        table_uri: str,
        table_name: str,
        hwm_write_mode: str = "overwrite",
    ) -> Optional[pl.DataFrame]:
        hwm_delta = self._get_delta(table_uri=table_uri, table_name=table_name)

        if isinstance(hwm_delta, DeltaTable):
            hwm_filter = hwm_delta.to_pyarrow_table()[0][0].as_py()
            logging.info(f"Setting new HWM, hwm_filter: {hwm_filter}")

            return df.filter(
                pl.col(self.sink_config.date_hwm_compare) > pl.lit(hwm_filter)
            )

        else:
            hwm_df = df.select(self.sink_config.date_hwm_compare).max()
            logging.info(f"Setting new HWM, hwm_filter: {hwm_df}")

            self._write_to_delta(
                df=hwm_df,
                mode=hwm_write_mode,
                table_uri=table_uri,
                table_name=table_name,
            )

    def _write_to_delta(
        self, df: pl.DataFrame, mode: str, table_uri: str, table_name: str
    ) -> None:
        try:
            write_deltalake(
                table_or_uri=f"{table_uri}/{table_name}",
                data=df.to_arrow(),
                mode=mode,  # type: ignore
                storage_options=self.storage_options,
                overwrite_schema=self.sink_config.overwrite_schema,
            )
            logging.info("Write Successful")

        except DeltaWriteError as delta_write_error:
            raise delta_write_error

    def execute(self, df: pl.DataFrame) -> None:
        table_uri = f"{self.sink_config.table_base_uri}"
        hwm_table_name = f"{self.sink_config.table_name}_hwm"
        table_name = self.sink_config.table_name

        if self.sink_config.hwm:
            filtered_df = self._filter_hwm(
                df=df,
                table_uri=table_uri,
                table_name=hwm_table_name,
            )

            if isinstance(filtered_df, pl.DataFrame):
                if not filtered_df.is_empty():
                    logging.info("Writing New Data!")
                    self._write_to_delta(
                        df=filtered_df,
                        mode=self.sink_config.mode,
                        table_uri=table_uri,
                        table_name=table_name,
                    )
                else:
                    logging.info("No New Data To Write!")

        else:
            self._write_to_delta(
                df=df,
                mode=self.sink_config.mode,
                table_uri=table_uri,
                table_name=table_name,
            )
