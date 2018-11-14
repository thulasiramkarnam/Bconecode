
import time
import json
import paramiko
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    """"
        * lambda function to start the instance and give the commands to execute program

    """
	
    ec2_client = boto3.client('ec2')
   
    # i-0b774eaa8e8a77c56 is the working instance now
    # i-0bbe7527407062453 is the ec2 instance id
    #time.sleep(60) # In order to make sure that the instance is running before giving commands
    s3_client = boto3.client('s3')
    s3_client.download_file('thulasi-ram-dum','ec2emrireland.pem', '/tmp/ec2.pem')
    s3 = boto3.resource('s3')
    object_acl = s3.ObjectAcl('input-thulasi','app_input_file.xlsx')
    response = object_acl.put(ACL='public-read')
    # to download ec2andemr.pem file from "thulasi-ram-bucket" bucket in to lambda temp folder
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privkey = paramiko.RSAKey.from_private_key_file('/tmp/ec2.pem')
    
    ssh.connect('ec2-34-248-198-186.eu-west-1.compute.amazonaws.com',username='ec2-user',pkey=privkey)
    # ssh connect to the ec2 server
    commands = ["wget -N https://s3-eu-west-1.amazonaws.com/input-thulasi/app_input_file.xlsx",
                    "wget -N https://s3-eu-west-1.amazonaws.com/thulasi-ram-dum/senseaipoc.py",
                  "python36 senseaipoc.py"]
    # List of commands to run on ubuntu server
    
    for command in commands:
        logger.info("executed command")
        ssh.exec_command(command)
        
