import uuid
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from app.storage.base import StorageBackend


class S3Storage(StorageBackend):
    def __init__(self, bucket_name: str, region_name: str) -> None:
        if not bucket_name:
            raise ValueError("S3 bucket name is required for S3Storage")

        self.bucket_name = bucket_name
        self.region_name = region_name
        self.s3_client = boto3.client("s3", region_name=self.region_name)

    def _generate_object_key(self, filename: str) -> str:
        file_extension = Path(filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        return f"uploads/{unique_filename}"

    async def save(self, file_bytes: bytes, filename: str) -> str:
        object_key = self._generate_object_key(filename)

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=file_bytes,
            )

            return object_key

        except ClientError as error:
            raise RuntimeError(f"Failed to upload file to S3: {error}") from error