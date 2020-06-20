#!/usr/bin/python3

import requests
import boto3
import sys

AWS_ACCESS_KEY_ID = sys.argv[1]
AWS_SECRET_ACCESS_KEY = sys.argv[2]
RECORD_NAME = sys.argv[3]
HOSTED_ZONE_ID = sys.argv[4]

def main():
    if get_current_public_ip() != get_current_record_value():
        print("Changing value...")
        change_record_value()
    else:
        print("No update needed.")   
        
def get_current_public_ip():
    response = requests.get("https://api.ipify.org?format=json")
    if response.status_code != 200:
        raise SystemExit("Could not resolve public IP")
    return response.json().get('ip')

def get_current_record_value():
    r53_client = boto3.client('route53', aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    records = r53_client.list_resource_record_sets(HostedZoneId=HOSTED_ZONE_ID)
    for _,x in enumerate(records.get('ResourceRecordSets')):
        if x.get('Name') == RECORD_NAME:
            value = x.get('ResourceRecords')[0].get('Value')
            return value
    raise SystemExit('Could not find record on AWS')

def change_record_value():
    r53_client = boto3.client('route53', aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    hosted_zone_id = HOSTED_ZONE_ID
    change_batch = {
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': RECORD_NAME,
                    'Type': 'A',                  
                    'TTL': 200,
                    'ResourceRecords': [
                        {
                            'Value': get_current_public_ip()
                        },
                    ]
                }
                
            },
        ]
    }

    return r53_client.change_resource_record_sets(HostedZoneId=hosted_zone_id,ChangeBatch=change_batch)

main()

