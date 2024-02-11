from dataclasses import dataclass


@dataclass(frozen=True)
class DeltaClientConfig:
    endpoint_url: str
    aws_s3_allow_unsafe_rename: str
