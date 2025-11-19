import boto3

# create a low level client
client = boto3.client('ec2')

# Step 1: Get ALL security group IDs
all_sgs_response = client.describe_security_groups()
all_sg_ids = set()  # We use a set for efficient lookups

for sg in all_sgs_response['SecurityGroups']:
    all_sg_ids.add(sg['GroupId'])  

# Step 2: Get USED security group IDs (from running instances)
used_sg_ids = set()
instances_response = client.describe_instances()

for reservation in instances_response['Reservations']:
    for instance in reservation['Instances']:
        for sg in instance['SecurityGroups']:  # Loop through SGs attached to this instance
            used_sg_ids.add(sg['GroupId'])  

# Step 3: Find UNUSED ones
unused_sg_ids = all_sg_ids - used_sg_ids

print("Unused Security Groups:")
for sg_id in unused_sg_ids:
    print(sg_id)

# After identifying unused_sg_ids, add this:

print(f"Found {len(unused_sg_ids)} unused security groups")

# SAFETY CHECK 1: Skip default security groups
unused_non_default_sgs = []
for sg_id in unused_sg_ids:
    # Get details to check if it's a default SG
    sg_detail = client.describe_security_groups(GroupIds=[sg_id])
    if sg_detail['SecurityGroups'][0]['GroupName'] != 'default':
        unused_non_default_sgs.append(sg_id)

print(f"After removing default SGs: {len(unused_non_default_sgs)} to delete")

# SAFETY CHECK 2: Dry run first
print("\n=== DRY RUN - Testing deletion (no changes will be made) ===")
for sg_id in unused_non_default_sgs:
    try:
        client.delete_security_group(GroupId=sg_id, DryRun=True)
        print(f" Would delete: {sg_id}")
    except Exception as e:
        print(f" Dry run failed for {sg_id}: {e}")

# SAFETY CHECK 3: Ask for confirmation before real deletion
response = input("\nProceed with actual deletion? (yes/no): ")
if response.lower() == 'yes':
    print("\n=== ACTUAL DELETION ===")
    for sg_id in unused_non_default_sgs:
        try:
            client.delete_security_group(GroupId=sg_id, DryRun=False)
            print(f" Deleted: {sg_id}")
        except Exception as e:
            print(f" Failed to delete {sg_id}: {e}")
else:
    print("Deletion cancelled")


