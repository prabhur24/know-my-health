# Know My Health (AWS)

"Know My Health" is a CLI tool designed to gather and visualize metrics from various AWS services, including EC2 instances, EBS volumes, ELB instances, and S3 buckets.

## Features

- **EC2 Instances**: List instances, display private IP, name, instance type, CPU usage, IO wait, RAM usage, and EBS details.
- **EBS Volumes**: List volumes, display size, state, volume type, IOPS, throughput, and attachment details.
- **ELB Instances**: List load balancers, display DNS name, scheme, type, state, listeners, and target group details.
- **S3 Buckets**: List buckets, display creation date, location, object count, total size, and ACL details.
- **Cost Data**: List AWS cost and usage data for a specified period.

## Setup

### Prerequisites

- Python 3.6+
- AWS CLI configured with the necessary permissions
- Virtual environment (optional but recommended)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/know-my-health.git
    cd know-my-health
    ```

2. **Create and activate a virtual environment** (optional):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install the package**:
    ```bash
    pip install -e .
    ```

### Configuration

Set up your AWS credentials using the AWS CLI:
```
know-my-health setup

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Sample Commands How it works :

1. EC2 Instances
Command:

know-my-health list-instances --profile default --bastion-ip 192.168.1.1 --key-path ~/.ssh/mykey.pem --visualize

Output:


+-------+-----------------+-------------------+----------------+---------+------------+--------------+--------------------------------------------------------+
| S.No  | Private IP      | Name              | Instance Type  | CPU (%) | IO Wait (%)| RAM Usage (%)| EBS Details                                            |
+-------+-----------------+-------------------+----------------+---------+------------+--------------+--------------------------------------------------------+
| 1     | 172.31.24.10    | web-server-1      | t2.micro       | 15.23   | 0.00       | 45.67 %      | /mnt: 5G used of 10G (50%)                             |
|       |                 |                   |                |         |            |              | /: 2G used of 8G (25%)                                 |
| 2     | 172.31.25.11    | database-server-1 | t3.medium      | 5.67    | 0.00       | 30.50 %      | /mnt: 10G used of 20G (50%)                            |
|       |                 |                   |                |         |            |              | /: 4G used of 16G (25%)                                |
+-------+-----------------+-------------------+----------------+---------+------------+--------------+--------------------------------------------------------+

2. EBS Volumes
Command:


know-my-health list-volumes --profile default --volume-type gp2

Output:


+-------+-----------------------+------------+--------+-------------+-------+------------+-------------------------------------+
| S.No  | Volume ID             | Size (GiB) | State  | Volume Type | IOPS  | Throughput | Attachments                         |
+-------+-----------------------+------------+--------+-------------+-------+------------+-------------------------------------+
| 1     | vol-0abcd1234efgh5678 | 100        | in-use | gp2         | 3000  | N/A        | i-0abcd1234efgh5678 (attached)      |
| 2     | vol-0abcd1234efgh5679 | 50         | in-use | gp2         | 1500  | N/A        | i-0abcd1234efgh5679 (attached)      |
+-------+-----------------------+------------+--------+-------------+-------+------------+-------------------------------------+

3. ELB Instances
Command:

know-my-health list-load-balancers --profile default --visualize

Output:


+-------+-------------------+-------------------------+---------+---------------------+------------------+------------+-----------------------+------------------------------------------------------------+
| S.No  | Name              | DNS Name                | Scheme  | Created Time        | Type             | State      | Listeners             | Target Groups                                              |
+-------+-------------------+-------------------------+---------+---------------------+------------------+------------+-----------------------+------------------------------------------------------------+
| 1     | my-load-balancer  | my-load-balancer-12345  | internet-facing | 2023-08-01T00:00:00Z | application    | active     | HTTP:80, HTTPS:443    | TG: tg-1, Healthy: 3, Unhealthy: 0, Requests: 1000, Successes: 950 |
| 2     | my-load-balancer2 | my-load-balancer2-12345 | internet-facing | 2023-08-01T00:00:00Z | network        | active     | TCP:80                | TG: tg-2, Healthy: 2, Unhealthy: 1, Requests: 500, Successes: 450  |
+-------+-------------------+-------------------------+---------+---------------------+------------------+------------+-----------------------+------------------------------------------------------------+

4. S3 Buckets
Command:

know-my-health list-buckets --profile default

Output:


+-------+-----------------------+---------------------+--------------+--------------+---------------------+----------------+------------------------------------------------------+
| S.No  | Name                  | Creation Date       | Location     | Object Count | Total Size (Bytes)  | Total Size (GB)| ACL                                                  |
+-------+-----------------------+---------------------+--------------+--------------+---------------------+----------------+------------------------------------------------------+
| 1     | my-bucket-1           | 2023-01-01T00:00:00Z| us-west-2    | 500          | 1073741824          | 1.00           | Grantee: my-user, Permission: FULL_CONTROL            |
|       |                       |                     |              |              |                     |                | Grantee: public, Permission: READ                     |
| 2     | my-bucket-2           | 2023-02-01T00:00:00Z| us-east-1    | 1500         | 2147483648          | 2.00           | Grantee: my-user, Permission: FULL_CONTROL            |
|       |                       |                     |              |              |                     |                | Grantee: public, Permission: READ                     |
+-------+-----------------------+---------------------+--------------+--------------+---------------------+----------------+------------------------------------------------------+

5. List AWS Cost and Usage Data

know-my-health list-cost --profile <profile> [options]

Options:

    --profile: AWS profile to use (default: default)
    --start-date: Start date for cost and usage report (YYYY-MM-DD)
    --end-date: End date for cost and usage report (YYYY-MM-DD)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Usage
General Command Structure

know-my-health <command> [options]

Commands
1. Setup AWS Configuration

know-my-health setup

This command will guide you through setting up your AWS credentials.
2. List EC2 Instances

know-my-health list-instances --profile <profile> [options]

Options:

    --profile: AWS profile to use (default: default)
    --tag: Tag key-value pair to filter instances (format: key:value)
    --instance-type: Instance type to filter instances
    --bastion-ip: Bastion server IP address
    --key-path: Path to SSH private key file
    --bastion-username: Username for bastion server (default: ec2-user)
    --visualize: Visualize the instance metrics

3. List EBS Volumes


know-my-health list-volumes --profile <profile> [options]

Options:

    --profile: AWS profile to use (default: default)
    --volume-type: Volume type to filter volumes
    --visualize: Visualize the volume metrics

4. List ELB Instances


know-my-health list-load-balancers --profile <profile> [options]

Options:

    --profile: AWS profile to use (default: default)
    --visualize: Visualize the load balancer metrics

5. List S3 Buckets

know-my-health list-buckets --profile <profile> [options]

Options:

    --profile: AWS profile to use (default: default)
    --visualize: Visualize the bucket metrics

Examples

List EC2 Instances with Details

know-my-health list-instances --profile default --bastion-ip 192.168.1.1 --key-path ~/.ssh/mykey.pem --visualize

Output:

+-------+-----------------+-------------------+----------------+---------+------------+--------------+--------------------------------------------------------+
| S.No  | Private IP      | Name              | Instance Type  | CPU (%) | IO Wait (%)| RAM Usage (%)| EBS Details                                            |
+-------+-----------------+-------------------+----------------+---------+------------+--------------+--------------------------------------------------------+
| 1     | 172.31.24.10    | web-server-1      | t2.micro       | 15.23   | 0.00       | 45.67 %      | /mnt: 5G used of 10G (50%)                             |
|       |                 |                   |                |         |            |              | /: 2G used of 8G (25%)                                 |
| 2     | 172.31.25.11    | database-server-1 | t3.medium      | 5.67    | 0.00       | 30.50 %      | /mnt: 10G used of 20G (50%)                            |
|       |                 |                   |                |         |            |              | /: 4G used of 16G (25%)                                |
+-------+-----------------+-------------------+----------------+---------+------------+--------------+--------------------------------------------------------+

List EBS Volumes of Type gp2

know-my-health list-volumes --profile default --volume-type gp2

Output:

+-------+-----------------------+------------+--------+-------------+-------+------------+-------------------------------------+
| S.No  | Volume ID             | Size (GiB) | State  | Volume Type | IOPS  | Throughput | Attachments                         |
+-------+-----------------------+------------+--------+-------------+-------+------------+-------------------------------------+
| 1     | vol-0abcd1234efgh5678 | 100        | in-use | gp2         | 3000  | N/A        | i-0abcd1234efgh5678 (attached)      |
| 2     | vol-0abcd1234efgh5679 | 50         | in-use | gp2         | 1500  | N/A        | i-0abcd1234efgh5679 (attached)      |
+-------+-----------------------+------------+--------+-------------+-------+------------+-------------------------------------+

List ELB Instances with Visualization

know-my-health list-load-balancers --profile default --visualize

Output:

+-------+-------------------+-------------------------+---------+---------------------+------------------+------------+-----------------------+------------------------------------------------------------+
| S.No  | Name              | DNS Name                | Scheme  | Created Time        | Type             | State      | Listeners             | Target Groups                                              |
+-------+-------------------+-------------------------+---------+---------------------+------------------+------------+-----------------------+------------------------------------------------------------+
| 1     | my-load-balancer  | my-load-balancer-12345  | internet-facing | 2023-08-01T00:00:00Z | application    | active     | HTTP:80, HTTPS:443    | TG: tg-1, Healthy: 3, Unhealthy: 0, Requests: 1000, Successes: 950 |
| 2     | my-load-balancer2 | my-load-balancer2-12345 | internet-facing | 2023-08-01T00:00:00Z | network        | active     | TCP:80                | TG: tg-2, Healthy: 2, Unhealthy: 1, Requests: 500, Successes: 450  |
+-------+-------------------+-------------------------+---------+---------------------+------------------+------------+-----------------------+------------------------------------------------------------+

List S3 Buckets

know-my-health list-buckets --profile default

Output:

+-------+-----------------------+---------------------+--------------+--------------+---------------------+----------------+------------------------------------------------------+
| S.No  | Name                  | Creation Date       | Location     | Object Count | Total Size (Bytes)  | Total Size (GB)| ACL                                                  |
+-------+-----------------------+---------------------+--------------+--------------+---------------------+----------------+------------------------------------------------------+
| 1     | my-bucket-1           | 2023-01-01T00:00:00Z| us-west-2    | 500          | 1073741824          | 1.00           | Grantee: my-user, Permission: FULL_CONTROL            |
|       |                       |                     |              |              |                     |                | Grantee: public, Permission: READ                     |
| 2     | my-bucket-2           | 2023-02-01T00:00:00Z| us-east-1    | 1500         | 2147483648          | 2.00           | Grantee: my-user, Permission: FULL_CONTROL            |
|       |                       |                     |              |              |                     |                | Grantee: public, Permission: READ                     |
+-------+-----------------------+---------------------+--------------+--------------+---------------------+----------------+------------------------------------------------------+

List AWS Cost and Usage Data

bash

know-my-health list-cost --profile default --start-date 2023-07-01 --end-date 2023-07-31

Output:

yaml

+-------+------------+--------------+
| S.No  | Date       | Amount (USD) |
+-------+------------+--------------+
| 1     | 2023-07-01 | 12.34        |
| 2     | 2023-07-02 | 11.56        |
| 3     | 2023-07-03 | 13.45        |
| 4     | 2023-07-04 | 12.78        |
| 5     | 2023-07-05 | 14.89        |
| ...   | ...        | ...          |
| 31    | 2023-07-31 | 15.67        |
+-------+------------+--------------+


Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
License.
