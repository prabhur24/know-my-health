import os
import click
import configparser
import boto3

CONFIG_DIR = os.path.expanduser("~/.know_my_health")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config")


def setup_config():
    """Setup AWS credentials and initial settings."""
    profile = click.prompt("Enter profile name", default="default")

    aws_access_key_id = click.prompt("Enter your AWS Access Key ID")
    aws_secret_access_key = click.prompt("Enter your AWS Secret Access Key")
    aws_region = click.prompt("Enter your AWS Region", default="us-east-1")

    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    config = configparser.ConfigParser()

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)

    if not config.has_section(profile):
        config.add_section(profile)

    config.set(profile, "aws_access_key_id", aws_access_key_id)
    config.set(profile, "aws_secret_access_key", aws_secret_access_key)
    config.set(profile, "aws_region", aws_region)

    with open(CONFIG_FILE, "w") as f:
        config.write(f)

    click.echo("Configuration saved successfully.")


def get_config(profile="default"):
    """Load configuration from the config file."""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    if profile not in config:
        raise click.ClickException("Profile '{}' not found in configuration file.".format(profile))

    return {
        "aws_access_key_id": config.get(profile, "aws_access_key_id"),
        "aws_secret_access_key": config.get(profile, "aws_secret_access_key"),
        "aws_region": config.get(profile, "aws_region")
    }


def get_boto3_client(service, profile="default"):
    """Get a boto3 client using the configured credentials."""
    config = get_config(profile)
    return boto3.client(
        service,
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
        region_name=config["aws_region"]
    )
