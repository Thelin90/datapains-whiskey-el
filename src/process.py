import polars as pl
from src.sink.write import Write
from src.source.extract import Extract


class Process:
    def __init__(self, extract: Extract, write: Write) -> None:
        self.extract = extract
        self.write = write

    def _set_hwm(self) -> None:
        pass

    def read(self) -> pl.DataFrame:
        return self.extract.fetch_from_api()

    def load(self, df: pl.DataFrame) -> None:
        self.write.execute(df=df)
