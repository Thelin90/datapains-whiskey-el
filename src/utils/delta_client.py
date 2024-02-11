import logging
import os
from typing import Dict, Optional
import polars as pl
from deltalake import DeltaTable, write_deltalake
from deltalake._internal import DeltaError

from src.models.delta_client_config import DeltaClientConfig


class DeltaClient:
    def __init__(self, delta_client_config: DeltaClientConfig) -> None:
        self.delta_client_config = delta_client_config
        self.storage_options = self._setup_storage_options()

    def _setup_storage_options(self) -> Dict[str, str]:
        try:
            os.environ[
                "AWS_S3_ALLOW_UNSAFE_RENAME"
            ] = self.delta_client_config.aws_s3_allow_unsafe_rename
            os.environ["AWS_STORAGE_ALLOW_HTTP"] = "1"
            os.environ["AWS_ALLOW_HTTP"] = "true"

            return {
                "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SECRET_ACCESS_KEY"],
                "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"],
                "AWS_REGION": os.environ["AWS_DEFAULT_REGION"],
                "AWS_ENDPOINT_URL": self.delta_client_config.endpoint_url,
            }
        except KeyError as key_error:
            raise key_error

    def get_delta_table(self, table_uri: str, table_name: str) -> Optional[DeltaTable]:
        try:
            table_uri = f"{table_uri}/{table_name}"
            delta_table = DeltaTable(
                storage_options=self.storage_options,
                table_uri=table_uri,
            )

            return delta_table

        except DeltaError as delta_client_error:
            logging.warning(f"Get Delta Client Error: {delta_client_error}")
            return None

    def write_to_delta(
        self,
        df: pl.DataFrame,
        mode: str,
        table_uri: str,
        table_name: str,
        overwrite_schema: bool,
    ) -> None:
        try:
            write_deltalake(
                table_or_uri=f"{table_uri}/{table_name}",
                data=df.to_arrow(),
                mode=mode,  # type: ignore
                storage_options=self.storage_options,
                overwrite_schema=overwrite_schema,
            )
            logging.info(
                f"Write Delta Client Successful, table: {table_name}, mode: {mode}"
            )

        except DeltaError as delta_write_error:
            logging.error(f"Write To Delta Client Error: {delta_write_error}")
            raise delta_write_error
