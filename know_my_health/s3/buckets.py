import click
from tabulate import tabulate
from ..config import get_boto3_client
from .visualize import visualize_buckets

def fetch_s3_buckets(profile="default"):
    """Fetch S3 buckets and list their details."""
    s3_client = get_boto3_client('s3', profile)
    response = s3_client.list_buckets()

    buckets = []
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        creation_date = bucket['CreationDate']

        # Fetching bucket metrics
        bucket_location = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        bucket_acl = s3_client.get_bucket_acl(Bucket=bucket_name)

        # Get the number of objects and total size in the bucket
        bucket_objects = s3_client.list_objects_v2(Bucket=bucket_name)
        total_size = 0
        object_count = 0

        if 'Contents' in bucket_objects:
            for obj in bucket_objects['Contents']:
                total_size += obj['Size']
                object_count += 1

        total_size_gb = total_size / (1024 ** 3)  # Convert bytes to GB

        buckets.append({
            'Name': bucket_name,
            'CreationDate': creation_date,
            'Location': bucket_location,
            'ACL': bucket_acl['Grants'],
            'ObjectCount': object_count,
            'TotalSizeBytes': total_size,
            'TotalSizeGB': total_size_gb
        })

    return buckets


def list_s3_buckets(profile="default", visualize=False):
    """List S3 buckets with details."""
    buckets = fetch_s3_buckets(profile)

    table = []
    for bucket in buckets:
        acl_info = "\n".join([
                                 f"Grantee: {grant['Grantee']['DisplayName'] if 'DisplayName' in grant['Grantee'] else 'N/A'}, Permission: {grant['Permission']}"
                                 for grant in bucket['ACL']])
        table.append([
            len(table) + 1, bucket['Name'], bucket['CreationDate'], bucket['Location'],
            bucket['ObjectCount'], bucket['TotalSizeBytes'], bucket['TotalSizeGB'], acl_info
        ])

    headers = ["S.No", "Name", "Creation Date", "Location", "Object Count", "Total Size (Bytes)", "Total Size (GB)",
               "ACL"]
    click.echo(tabulate(table, headers, tablefmt="grid"))

    if visualize:
        visualize_buckets(buckets)
