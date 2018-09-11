

import json
import paramiko
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    # TODO implement
    logger.info(event)
    logger.info("After event")
    #id = i-058481edd4788c01c
    s3_client = boto3.client('s3')
    s3_client.download_file('thulasi-ram-dum','ec2andemr.pem', '/tmp/ec2.pem')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file('/tmp/ec2.pem')
    ssh.connect('ec2-18-221-144-29.us-east-2.compute.amazonaws.com',username='ec2-user',pkey=privkey)
    commands = ["wget -N https://s3-eu-west-1.amazonaws.com/thulasi-ram-dum/raw_material_final_11.py",
                  "python36 raw_material_final_11.py"]
    for command in commands:
        ssh.exec_command(command)
        
	
	
	

