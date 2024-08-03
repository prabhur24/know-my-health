import click
from tabulate import tabulate
from datetime import datetime, timedelta
from ..config import get_boto3_client


def fetch_cost_and_usage(profile="default", start_date=None, end_date=None):
    """Fetch cost and usage data from AWS Cost Explorer."""
    ce_client = get_boto3_client('ce', profile)

    if not start_date:
        start_date = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.utcnow().strftime('%Y-%m-%d')

    response = ce_client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
    )

    results = []
    for result in response['ResultsByTime']:
        date = result['TimePeriod']['Start']
        amount = result['Total']['UnblendedCost']['Amount']
        results.append({
            'Date': date,
            'Amount': float(amount)
        })

    return results


def list_cost_and_usage(profile="default", start_date=None, end_date=None):
    """List cost and usage data."""
    costs = fetch_cost_and_usage(profile, start_date, end_date)

    table = []
    for cost in costs:
        table.append([
            len(table) + 1, cost['Date'], cost['Amount']
        ])

    headers = ["S.No", "Date", "Amount (USD)"]
    click.echo(tabulate(table, headers, tablefmt="grid"))
