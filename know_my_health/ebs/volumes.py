import click
from tabulate import tabulate
from ..config import get_boto3_client
from .visualize import visualize_volumes

def fetch_ebs_volumes(profile="default", volume_type=None):
    """Fetch EBS volumes and list their details."""
    ec2_client = get_boto3_client('ec2', profile)

    filters = []
    if volume_type:
        filters.append({
            'Name': 'volume-type',
            'Values': [volume_type]
        })

    response = ec2_client.describe_volumes(Filters=filters)

    volumes = []
    for volume in response['Volumes']:
        volume_id = volume['VolumeId']
        size = volume['Size']
        state = volume['State']
        volume_type = volume['VolumeType']
        iops = volume.get('Iops', 'N/A')
        throughput = volume.get('Throughput', 'N/A')
        attachments = volume['Attachments']
        attachment_details = ', '.join(
            [f"{attachment['InstanceId']} ({attachment['State']})" for attachment in attachments])

        volumes.append({
            'VolumeId': volume_id,
            'Size': size,
            'State': state,
            'VolumeType': volume_type,
            'Iops': iops,
            'Throughput': throughput,
            'Attachments': attachment_details
        })

    # Sort by VolumeType by default
    volumes.sort(key=lambda x: x['VolumeType'])
    return volumes


def list_ebs_volumes(profile="default", volume_type=None, visualize=False):
    """List EBS volumes with details."""
    volumes = fetch_ebs_volumes(profile, volume_type)

    table = []
    for volume in volumes:
        table.append([
            len(table) + 1, volume['VolumeId'], volume['Size'], volume['State'], volume['VolumeType'],
            volume['Iops'], volume['Throughput'], volume['Attachments']
        ])

    headers = ["S.No", "Volume ID", "Size (GiB)", "State", "Volume Type", "IOPS", "Throughput", "Attachments"]
    click.echo(tabulate(table, headers, tablefmt="grid"))

    if visualize:
        visualize_volumes(volumes)
