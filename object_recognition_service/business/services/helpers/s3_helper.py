import os
from uuid import uuid4
from pathlib import Path

import aioboto3
from botocore.exceptions import ClientError


async def upload_image_to_s3(
    file_content: bytes,
    file_name: str,
    mime_type: str,
    bucket_name: str,
    region_name: str,
) -> str:
    ext = Path(file_name).suffix  # e.g. ".jpg"
    object_key = f"{uuid4()}{ext}"

    session = aioboto3.Session()
    async with session.client("s3", region_name=region_name) as s3_client:
        try:
            await s3_client.put_object(
                Bucket=bucket_name,
                Key=object_key,
                Body=file_content,
                ContentType=mime_type,
            )
        except ClientError as e:
            raise RuntimeError(f"Failed to upload image to S3: {e}") from e

    return object_key

async def download_image_from_s3(
    object_key: str,
    bucket_name: str,
    region_name: str,
) -> bytes:
    session = aioboto3.Session()
    async with session.client("s3", region_name=region_name) as s3_client:
        try:
            response = await s3_client.get_object(
                Bucket=bucket_name,
                Key=object_key,
            )
            async with response["Body"] as stream:
                file_content = await stream.read()
        except ClientError as e:
            if e.response["Error"]["Code"] in ("NoSuchKey", "404"):
                raise FileNotFoundError(f"Object not found in S3: {object_key}") from e
            raise RuntimeError(f"Failed to download image from S3: {e}") from e

    return file_content