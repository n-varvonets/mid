# Program by Nick Varvonets
# Lambda Function to Create S3 Bucket

# Version         Date         Info
# 1.0             2017         Initial Version

import boto3, os, time
import json

AWS_DEFAULT_REGION = "eu-west-1"  # Region where Lambda is running
os.environ['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION

bucketname = "lambda.created.me.on-" + str(time.time())


def lambda_handler(event, context):
    myS3 = boto3.resource('s3')

    try:
        results = myS3.create_bucket(
            Bucket=bucketname,
            CreateBucketConfiguration={'LocationConstraint': AWS_DEFAULT_REGION}
        )
        print("<h1><font color=green>S3 Bucket Created Successfully:</font></h1><br><br>" + str(results))
    except:
        print("<h1><font color=red>Error!</font></h1><br><br>")


# -------------------------------------------------------------

# Program by Denis Astahov
# Lambda Function to List S3 Buckets

# Version         Date         Info
# 1.0             2017         Initial Version

import boto3, os


def lambda_handler(event, context):
    myS3 = boto3.client('s3')

    try:
        results = myS3.list_buckets()
        print(results)
        output = ""
        for bucket in results['Buckets']:
            output = output + bucket['Name'] + "\n"
        print("<h1><font color=green>S3 Bucket List:</font></h1><br><br>" + output)
    except:
        print("<h1><font color=red>Error!</font></h1><br><br>")
