import boto3
from botocore.exceptions import ClientError


def get_s3_client(profile: str | None = None):
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    return session.client("s3")


def get_presigned_url(
    bucket_name: str, upload_path: str, profile: str | None = None, expiration: int = 3600
) -> str | None:
    """
    Generate a presigned URL to upload a file to S3.

    Args:
        bucket_name (str): Name of the S3 bucket.
        upload_path (str): Path in the S3 bucket to upload to (including the CSV file).
        profile (str, optional): AWS profile name. Defaults to None and default AWS profile.
        expiration (int, optional):
          Time in seconds for the presigned URL to remain valid. Defaults to 3600.

    Returns:
        str: Presigned URL as a string. None if error occurs.
    """
    s3_client = get_s3_client(profile=profile)

    try:
        response = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket_name, "Key": upload_path},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None

    return response
