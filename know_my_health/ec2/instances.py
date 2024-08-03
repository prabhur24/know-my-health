import click
from tabulate import tabulate
import paramiko
from paramiko import SSHClient, AutoAddPolicy
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..config import get_boto3_client
from .visualize import visualize_instance_metrics


def get_instance_metrics_via_ssh(instance, bastion_ip, key_path, bastion_username='ec2-user',
                                 target_username='ec2-user'):
    """Fetch instance metrics via SSH using the sar and df -H commands through a bastion server."""
    instance_id = instance['InstanceId']
    private_ip = instance.get('PrivateIpAddress', 'N/A')

    bastion = SSHClient()
    bastion.set_missing_host_key_policy(AutoAddPolicy())

    try:
        # Connect to bastion server
        bastion.connect(bastion_ip, username=bastion_username, key_filename=key_path)

        # Setup proxy command
        bastion_transport = bastion.get_transport()
        dest_addr = (private_ip, 22)
        local_addr = ('127.0.0.1', 22)
        channel = bastion_transport.open_channel("direct-tcpip", dest_addr, local_addr)

        # Connect to target instance through bastion
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(private_ip, username=target_username, key_filename=key_path, sock=channel)

        # Run the sar command for CPU and RAM usage
        stdin, stdout, stderr = ssh.exec_command("sar -u 1 1 | grep Average")
        cpu_output = stdout.read().decode()
        stdin, stdout, stderr = ssh.exec_command("sar -r 1 1 | grep Average")
        ram_output = stdout.read().decode()

        # Extract CPU and RAM usage
        columns = cpu_output.split()
        cpu_usage = 100 - float(columns[7])  # %idle is the eighth column, so CPU usage is 100 - %idle
        iowait = float(columns[5])  # %iowait is the sixth column
        ram_usage = float(ram_output.split()[3])  # %memused is the fourth column

        # Run the df -H command for EBS volumes
        stdin, stdout, stderr = ssh.exec_command("df -H | grep '^/dev'")
        ebs_output = stdout.read().decode()

        ebs_volumes = []
        for line in ebs_output.strip().split("\n"):
            parts = line.split()
            if len(parts) >= 6:
                filesystem, size, used, avail, percent, mountpoint = parts[:6]
                ebs_volumes.append({
                    'Filesystem': filesystem,
                    'Size': size,
                    'Used': used,
                    'Available': avail,
                    'Use%': percent,
                    'Mountpoint': mountpoint
                })

        ssh.close()
        return instance_id, cpu_usage, iowait, ram_usage, ebs_volumes
    except Exception as e:
        return instance_id, None, None, None, []
    finally:
        bastion.close()


def fetch_ec2_instances(profile="default", tags=None, instance_type=None):
    """Fetch EC2 instances and list their details."""
    ec2_client = get_boto3_client('ec2', profile)

    filters = [
        {'Name': 'instance-state-name', 'Values': ['running']}
    ]
    if tags:
        for tag in tags:
            key, value = tag.split(':')
            filters.append({
                'Name': 'tag:{}'.format(key),
                'Values': [value]
            })
    if instance_type:
        filters.append({
            'Name': 'instance-type',
            'Values': [instance_type]
        })

    response = ec2_client.describe_instances(Filters=filters)

    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            private_ip = instance.get('PrivateIpAddress', 'N/A')
            name_tag = 'N/A'
            instance_type = instance.get('InstanceType', 'N/A')
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name':
                    name_tag = tag['Value']
                    break
            instances.append({
                'InstanceId': instance_id,
                'PrivateIpAddress': private_ip,
                'Name': name_tag,
                'InstanceType': instance_type
            })
    return instances


def list_ec2_instances(profile="default", tags=None, instance_type=None, bastion_ip=None, key_path=None,
                       bastion_username='ec2-user',visualize=False):
    """List EC2 instances with details."""
    instances = fetch_ec2_instances(profile, tags, instance_type)

    table = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(get_instance_metrics_via_ssh, instance, bastion_ip, key_path, bastion_username): instance
            for instance in instances}

        for future in as_completed(futures):
            instance = futures[future]
            try:
                instance_id, cpu_usage, iowait, ram_usage, ebs_volumes = future.result()
                instance['CPUUtilization'] = cpu_usage if cpu_usage is not None else 'N/A'
                instance['IOWait'] = iowait if iowait is not None else 'N/A'
                instance['RAMUsage'] = ram_usage if ram_usage is not None else 'N/A'
                instance['EBSVolumes'] = ebs_volumes
            except Exception as e:
                instance['CPUUtilization'] = 'N/A'
                instance['IOWait'] = 'N/A'
                instance['RAMUsage'] = 'N/A'
                instance['EBSVolumes'] = []

            ebs_details = "\n".join(
                [f"{vol['Mountpoint']}: {vol['Used']} used of {vol['Size']} ({vol['Use%']})" for vol in
                 instance['EBSVolumes']])
            table.append([
                len(table) + 1, instance['PrivateIpAddress'], instance['Name'], instance['InstanceType'],
                "{:.2f}".format(instance['CPUUtilization']) if instance['CPUUtilization'] != 'N/A' else 'N/A',
                "{:.2f}".format(instance['IOWait']) if instance['IOWait'] != 'N/A' else 'N/A',
                "{:.2f} %".format(instance['RAMUsage']) if instance['RAMUsage'] != 'N/A' else 'N/A',  # Show % used
                ebs_details
            ])

    # Sort the table by CPU utilization and RAM usage
    table.sort(key=lambda x: (float(x[4]) if x[4] != 'N/A' else -1, float(x[6].split()[0]) if x[6] != 'N/A' else -1),
               reverse=True)

    headers = ["S.No", "Private IP", "Name", "Instance Type", "CPU (%)", "IO Wait (%)", "RAM Usage (%)", "EBS Details"]
    click.echo(tabulate(table, headers, tablefmt="grid"))
    if visualize:
        visualize_instance_metrics(instances)
