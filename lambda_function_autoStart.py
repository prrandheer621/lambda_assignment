import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')

    # Describe instances with specific tags
    response = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Stop']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    # Stop instances with Auto-Stop tag
    auto_stop_instances = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
    ]

    if auto_stop_instances:
        ec2_client.stop_instances(InstanceIds=auto_stop_instances)
        print(f"Stopped instances: {auto_stop_instances}")

    # Describe instances with Auto-Start tag
    response = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Start']},
            {'Name': 'instance-state-name', 'Values': ['stopped']}
        ]
    )

    # Start instances with Auto-Start tag
    auto_start_instances = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
    ]
    if auto_start_instances:
        ec2_client.start_instances(InstanceIds=auto_start_instances)
        print(f"Started instances: {auto_start_instances}")

    return {
        'statusCode': 200,
        'body': 'EC2 instances managed successfully!'
    }
