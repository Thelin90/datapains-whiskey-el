import logging
import sys

from src.models.application_config import ApplicationConfig, Config
from src.process import Process
from src.sink.write import Write
from src.source.extract import Extract
from src.utils.delta_client import DeltaClient
from src.utils.parser import Parser

if __name__ == "__main__":
    parser = Parser()

    application_config: ApplicationConfig = Config(
        config=parser.read(file_path=parser.get_args().config_file_name)
    ).set_application_config()

    if application_config:
        logging.basicConfig(
            stream=sys.stdout,
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=application_config.base_config.log_level,
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        raise ValueError("Could not setup application config!")

    extract = Extract(api_config=application_config.api_config)
    delta_client = DeltaClient(
        delta_client_config=application_config.delta_client_config
    )

    write = Write(
        sink_config=application_config.sink_config,
        delta_client=delta_client,
    )

    process = Process(extract=extract, write=write)

    df = process.read()
    process.load(df=df)
