import click
from tabulate import tabulate
from ..config import get_boto3_client
import datetime
from .visualize import visualize_load_balancers


def fetch_classic_elbs(profile="default"):
    """Fetch classic ELBs and list their details."""
    elb_client = get_boto3_client('elb', profile)

    response = elb_client.describe_load_balancers()

    load_balancers = []
    for elb in response['LoadBalancerDescriptions']:
        elb_name = elb['LoadBalancerName']
        dns_name = elb['DNSName']
        scheme = elb['Scheme']
        created_time = elb['CreatedTime']
        instances = ', '.join([instance['InstanceId'] for instance in elb['Instances']])
        listeners = ', '.join(
            [f"{listener['Listener']['Protocol']}:{listener['Listener']['LoadBalancerPort']}" for listener in
             elb['ListenerDescriptions']])

        load_balancers.append({
            'Name': elb_name,
            'DNSName': dns_name,
            'Scheme': scheme,
            'CreatedTime': created_time,
            'Instances': instances,
            'Listeners': listeners,
            'Type': 'Classic ELB'
        })
    return load_balancers


def fetch_target_group_metrics(elbv2_client, target_group_arn):
    """Fetch target group metrics such as health and request count."""
    # Get target health
    health_response = elbv2_client.describe_target_health(TargetGroupArn=target_group_arn)
    healthy_count = sum(
        1 for target in health_response['TargetHealthDescriptions'] if target['TargetHealth']['State'] == 'healthy')
    unhealthy_count = sum(
        1 for target in health_response['TargetHealthDescriptions'] if target['TargetHealth']['State'] != 'healthy')

    # Assume that request count and success count metrics are collected via CloudWatch (simplified example)
    # Note: Replace with actual CloudWatch metric fetching code if needed.
    request_count = 0
    success_count = 0

    return healthy_count, unhealthy_count, request_count, success_count


def fetch_v2_elbs(profile="default"):
    """Fetch ALBs/NLBs and list their details."""
    elbv2_client = get_boto3_client('elbv2', profile)

    response = elbv2_client.describe_load_balancers()

    load_balancers = []
    for elb in response['LoadBalancers']:
        elb_name = elb['LoadBalancerName']
        dns_name = elb['DNSName']
        scheme = elb['Scheme']
        created_time = elb['CreatedTime']
        elb_type = elb['Type']
        state = elb['State']['Code']
        listeners = ', '.join([f"{listener['Protocol']}:{listener['Port']}" for listener in
                               elbv2_client.describe_listeners(LoadBalancerArn=elb['LoadBalancerArn'])['Listeners']])

        # Fetch target groups associated with the load balancer
        target_groups = elbv2_client.describe_target_groups(LoadBalancerArn=elb['LoadBalancerArn'])['TargetGroups']
        target_group_details = []
        for tg in target_groups:
            tg_name = tg['TargetGroupName']
            tg_arn = tg['TargetGroupArn']
            healthy_count, unhealthy_count, request_count, success_count = fetch_target_group_metrics(elbv2_client,
                                                                                                      tg_arn)
            target_group_details.append({
                'TargetGroupName': tg_name,
                'HealthyCount': healthy_count,
                'UnhealthyCount': unhealthy_count,
                'RequestCount': request_count,
                'SuccessCount': success_count
            })

        load_balancers.append({
            'Name': elb_name,
            'DNSName': dns_name,
            'Scheme': scheme,
            'CreatedTime': created_time,
            'State': state,
            'Listeners': listeners,
            'Type': elb_type,
            'TargetGroups': target_group_details
        })
    return load_balancers


def fetch_elb_instances(profile="default"):
    """Fetch both classic and v2 ELB instances and list their details."""
    classic_elbs = fetch_classic_elbs(profile)
    v2_elbs = fetch_v2_elbs(profile)
    return classic_elbs + v2_elbs


def list_elb_instances(profile="default", visualize=False):
    """List ELB instances with details."""
    load_balancers = fetch_elb_instances(profile)

    table = []
    for lb in load_balancers:
        target_groups_info = "\n".join([
            f"TG: {tg['TargetGroupName']}, Healthy: {tg['HealthyCount']}, Unhealthy: {tg['UnhealthyCount']}, Requests: {tg['RequestCount']}, Successes: {tg['SuccessCount']}"
            for tg in lb.get('TargetGroups', [])
        ])
        table.append([
            len(table) + 1, lb['Name'], lb['DNSName'], lb['Scheme'], lb['CreatedTime'],
            lb['Type'], lb.get('State', 'N/A'), lb['Listeners'], target_groups_info
        ])

    headers = ["S.No", "Name", "DNS Name", "Scheme", "Created Time", "Type", "State", "Listeners", "Target Groups"]
    click.echo(tabulate(table, headers, tablefmt="grid"))

    if visualize:
        visualize_load_balancers(load_balancers)
