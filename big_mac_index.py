import boto3
import json
import requests
import os
from decouple import config


NASDAQ_DATA_API_KEY = config("NASDAQ_DATA_API_KEY")
S3_AWS_BUCKET = config("S3_AWS_BUCKET")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")


class ClientS3PutObject:

    def __init__(self, bucket, file_name, country):
        self.bucket = bucket
        self.file_name = file_name
        self.country = country

    # Creating the low level functional client to connect with AWS S3.
    def create_s3_client(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
            region_name='eu-central-1'
        )

    def api_get_requests(self):
    #Set params for API requests
        params = {"start_date": "2021-07-31",
                "end_date": "2021-07-31",
                "api_key":NASDAQ_DATA_API_KEY
                }
    # Do requests into API NASDAQ using params
        data = requests.get(f'https://data.nasdaq.com/api/v3/datasets/ECONOMIST/BIGMAC_{self.country}', params=params)
        return data.json()

    # Change to json file and save into local dictionary
    def save_json_file_local_dir(self):

        with open(self.file_name, 'w') as f:
            json.dump(self.api_get_requests(), f)


    # Put object(created json file) to AWS S3
    def s3_s3_put_object(self):
        self.response = self.s3_client.put_object(
            Bucket=self.bucket,
            Key=self.file_name,
            Body=json.dumps(self.api_get_requests())
            )

    def check_status_process(self):
        status = self.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status == 200:
            print(f"Successful S3 put_object response. Status - {status}")
        else:
            print(f"Unsuccessful S3 put_object response. Status - {status}")

    def run(self):
        self.create_s3_client()
        self.api_get_requests()
        self.s3_s3_put_object()
        self.check_status_process()

if __name__ == "__main__":
    client = ClientS3PutObject(S3_AWS_BUCKET, "", "POL")
    client.run()



