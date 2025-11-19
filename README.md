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



