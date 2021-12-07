import json
import boto3


def lambda_handler(event, context):
    action = event["Records"][0].get("eventName", None)
    ip = event["Records"][0].get("requestParameters", {}).get("sourceIPAddress", None)
    bucket_name = event["Records"][0].get("s3", {}).get("bucket", {}).get("name", None)
    object = event["Records"][0].get("s3", {}).get("object", {}).get("key", None)
    event_time = event["Records"][0].get("eventTime", None)

    client = boto3.client("ses")

    subject = f"{action} event from  {bucket_name}."
    body = f"""
        <br>
        <p>This email is to notify you that {action}.</p>
        <p>Object: {object}.</p>
        <p>Event time: {event_time}.</p>
        <p>Source IP: {ip}.</p
        """

    message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}

    response = client.send_email(Source="victor.wijatkowski@gmail.com",
                                 Destination={"ToAddresses": ["victor.wijatkowski@gmail.com"]}, Message=message)

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    if status == 200:
        return {f'Successful: Status code {status}'}
    else:
        return {f'Unsuccessful: Status code {status}'}