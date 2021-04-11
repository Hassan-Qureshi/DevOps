"""
This lambda functions was to be used as event trigger
It runs as cloudwatch alarm and as soon as the memory crosses the threshold,
it trigger this lambda using SNS which runs SSM to run commmand on EC2 instance
to clean the un-used processes
"""

import logging
import boto3
import botocore
import time
event = eval(str)

msg = event.get('Records')[0]['Sns']['Message']
msg = eval(msg.replace('null', '""'))
dimensions = msg.get('Trigger')['Dimensions']
instance_id = -1
for dimension in dimensions:
    if dimension.get('name') == 'InstanceId':
        instance_id = dimension.get('value')
print(instance_id)

client = boto3.client('ssm')

response = client.send_command(
    InstanceIds=[instance_id],
    DocumentName='AWS-RunShellScript',
    Parameters={
        'commands': [
            'sudo apachectl -k restart'
        ]
    })
    
command_id = response['Command']['CommandId']
tries = 0
output = 'False'
while tries < 10:
    tries = tries + 1
    try:
        time.sleep(0.5)  # some delay always required...
        result = client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        if result['Status'] == 'InProgress':
            continue
        output = result['StandardOutputContent']
        break
    except client.exceptions.InvocationDoesNotExist:
        continue
print(output)