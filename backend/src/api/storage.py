from botocore.config import Config
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class TimeoutS3Boto3Storage(S3Boto3Storage):
    config = Config(
        connect_timeout=settings.S3_NETWORK_CONNECTION_TIMEOUT_SECONDS,
        read_timeout=settings.S3_NETWORK_READ_TIMEOUT_SECONDS,
        retries={
            "max_attempts": settings.S3_NETWORK_RETRY_COUNT,
        },
    )
