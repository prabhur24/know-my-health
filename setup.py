from setuptools import setup, find_packages

setup(
    name="know-my-health",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "click",
        "matplotlib"
    ],
    entry_points={
        "console_scripts": [
            "know-my-health=know_my_health.cli:cli",
        ],
    },
)
