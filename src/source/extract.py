import logging

import polars as pl
from requests import request
from requests.exceptions import ConnectionError

from src.models.api_config import ApiConfig


class RequestErrors(
    ConnectionError,
):
    pass


class Extract:
    def __init__(self, api_config: ApiConfig) -> None:
        self.api_config = api_config

    def _enforce_date(
        self, df: pl.DataFrame, date_format: str = "%Y-%m-%d"
    ) -> pl.DataFrame:
        parse_date_column = self.api_config.parse_date_column

        if parse_date_column in df.columns:
            df = df.with_columns(
                pl.col(self.api_config.parse_date_column).str.strptime(
                    pl.Date, date_format
                )
            )

        return df

    def fetch_from_api(self, operation: str = "GET") -> pl.DataFrame:
        try:
            api_url_with_format = (
                f"{self.api_config.url}/?format={self.api_config.output}"
            )

            logging.info(f"FETCH FROM API: {api_url_with_format}")

            response = request(
                operation,
                api_url_with_format,
            )

            json_data = response.json()

            return self._enforce_date(df=pl.from_dicts(data=json_data))

        except RequestErrors as request_error:
            raise request_error
