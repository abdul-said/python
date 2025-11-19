# AWS Security Group Cleanup Script

A safety-first Python script to identify and remove unused AWS Security Groups, helping to maintain a clean and secure cloud environment.

## 🚀 Features

- **Identifies Unused Security Groups**: Automatically detects SGs not attached to any running EC2 instances
- **Safety-First Approach**: Implements multiple safety measures to prevent accidental deletion
- **Dry Run Mode**: Tests deletions without making any changes
- **Default SG Protection**: Automatically skips default security groups
- **Interactive Confirmation**: Requires manual approval before any deletion
- **Error Handling**: Robust error handling for AWS API calls

## 🛠️ Prerequisites

- Python 3.6+
- boto3 library (`pip install boto3`)
- AWS credentials configured (via AWS CLI, IAM role, or environment variables)
- IAM permissions: `ec2:DescribeSecurityGroups`, `ec2:DescribeInstances`, `ec2:DeleteSecurityGroup`

## 📋 IAM Policy Requirements

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeInstances"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow", 
            "Action": "ec2:DeleteSecurityGroup",
            "Resource": "*",
            "Condition": {
                "StringNotEquals": {
                    "ec2:ResourceTag/purpose": "protected"
                }
            }
        }
    ]
}

# Usage

## Clone repo
git clone https://github.com/yourusername/aws-sg-cleanup.git
cd aws-sg-cleanup

## Install dependencies
pip install boto3

## Run the script
python cleanup.py

# 🔒 Safety Features
Dry Run First: The script always performs a dry run showing what would be deleted

Default SG Protection: Default security groups are automatically excluded

Manual Confirmation: Explicit user confirmation required before any deletion

Error Handling: Continues processing even if individual deletions fail

# 📝 Example Output

Found 8 unused security groups
After removing default SGs: 6 to delete

=== DRY RUN - Testing deletion (no changes will be made) ===
✓ Would delete: sg-070f22e3fe90e3642
✓ Would delete: sg-0a1b2c3d4e5f67890

Proceed with actual deletion? (yes/no): yes

=== ACTUAL DELETION ===
✓ Deleted: sg-070f22e3fe90e3642
✓ Deleted: sg-0a1b2c3d4e5f67890

# 🎯 How It Works
Discovery: Fetches all security groups in the AWS account

Usage Analysis: Identifies SGs currently attached to running EC2 instances

Comparison: Uses Python sets to find unused SGs (all SGs - used SGs)

Safety Checks: Removes default SGs and performs dry run

Execution: Deletes unused SGs after user confirmation

# ⚠️ Important Notes
Test First: Always run in a non-production environment first

Regional Scope: Currently works in a single AWS region (defaults to your AWS configuration)

EC2 Only: Currently only checks EC2 instances (does not check ELB, RDS, Lambda, etc.)

Backup: Consider taking backups or snapshots before running in production

# 🚧 Limitations & Future Enhancements
Add support for checking other AWS services (ELB, RDS, Lambda)

Multi-region support

Tag-based exclusion (e.g., skip SGs with protect: true tags)

CloudWatch metrics and logging

Scheduled execution via AWS Lambda

# 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

# 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

