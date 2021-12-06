#This lambda function was implemented into AWS LAMBDA

import json
import boto3


def lambda_handler(event, context):

    action = event["Records"][0].get("eventName", None)
    ip = event["Records"][0].get("requestParameters", {}).get("sourceIPAddress", None)
    bucket_name = event["Records"][0].get("s3", {}).get("bucket", {}).get("name", None)
    object = event["Records"][0].get("s3", {}).get("object", {}).get("key", None)

    client = boto3.client("ses")

    subject = str(action) + 'Event from' + bucket_name
    body = """
        <br>
        This email is to notify you that {} event.\n
        Object {}.\n
        Source IP: {}
    """.format(action, object, ip)

    message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}

    response = client.send_email(Source="victor.wijatkowski@gmail.com",
                                 Destination={"ToAddresses": ["monika.kulisz@onwelo.com"]}, Message=message)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }