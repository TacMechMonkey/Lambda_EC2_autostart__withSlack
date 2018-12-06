import boto3
import json
import requests

region = 'ap-southeast-2'
ec2 = boto3.resource('ec2', region_name=region)
key_name = 'Use'
key_id = 'Production'
webhook_url = "https://hooks.slack.com/services/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yE"

def inst_poll():
    stopped_instances = ec2.instances.filter(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['stopped']},
            {'Name': ('tag:'+key_name), 'Values': [key_id]}
        ]
    )
    
    for instance in stopped_instances:
        instance.start()
        inst_id = instance.id
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                inst_name = tag['Value']
        notification(inst_name, inst_id)

def notification(inst_name, inst_id):
    slack_data = {'text': "Started stopped instance: " + inst_name + ", instance ID: " + inst_id}
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    
    print(response)

def lambda_handler(event, context):
    inst_poll()
    return "Successful"
