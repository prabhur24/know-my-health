import click
from .config import setup_config
from .ec2.instances import list_ec2_instances
from .ebs.volumes import list_ebs_volumes
from .elb.load_balancers import list_elb_instances
from .s3.buckets import list_s3_buckets
from .cost.cost_explorer import list_cost_and_usage

@click.group()
def cli():
    """Know My Health CLI"""
    pass

@cli.command()
def setup():
    """Setup AWS credentials and initial settings."""
    setup_config()

@cli.command()
@click.option('--profile', default='default', help='AWS profile to use')
@click.option('--tag', multiple=True, help='Tag key-value pair to filter instances, format: key:value')
@click.option('--instance-type', help='Instance type to filter instances')
@click.option('--bastion-ip', required=True, help='Bastion server IP address')
@click.option('--key-path', required=True, help='Path to SSH private key file')
@click.option('--bastion-username', default='ec2-user', help='Username for bastion server')
@click.option('--visualize', is_flag=True, help='Visualize the instance metrics')
def list_instances(profile, tag, instance_type, bastion_ip, key_path, bastion_username, visualize):
    """List EC2 instances with Private IP, Name tag, and Instance Type."""
    list_ec2_instances(profile, tag, instance_type, bastion_ip, key_path, bastion_username, visualize)

@cli.command()
@click.option('--profile', default='default', help='AWS profile to use')
@click.option('--volume-type', help='Volume type to filter volumes')
@click.option('--visualize', is_flag=True, help='Visualize the volume metrics')
def list_volumes(profile, volume_type, visualize):
    """List EBS volumes with details."""
    list_ebs_volumes(profile, volume_type, visualize)

@cli.command()
@click.option('--profile', default='default', help='AWS profile to use')
@click.option('--visualize', is_flag=True, help='Visualize the load balancer metrics')
def list_load_balancers(profile, visualize):
    """List ELB instances with details."""
    list_elb_instances(profile, visualize)

@cli.command()
@click.option('--profile', default='default', help='AWS profile to use')
@click.option('--visualize', is_flag=True, help='Visualize the bucket metrics')
def list_buckets(profile, visualize):
    """List S3 buckets with details."""
    list_s3_buckets(profile, visualize)

@cli.command()
@click.option('--profile', default='default', help='AWS profile to use')
@click.option('--start-date', help='Start date for cost and usage report (YYYY-MM-DD)')
@click.option('--end-date', help='End date for cost and usage report (YYYY-MM-DD)')
def list_cost(profile, start_date, end_date):
    """List AWS cost and usage data."""
    list_cost_and_usage(profile, start_date, end_date)

if __name__ == "__main__":
    cli()
