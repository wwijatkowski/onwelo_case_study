import boto3
import json
import requests
from decouple import config


NASDAQ_DATA_API_KEY = config("NASDAQ_DATA_API_KEY")
S3_AWS_BUCKET = config("S3_AWS_BUCKET")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")


class RequestsBigMacIndexApi:

    def __init__(self, country):
        self.country = country

    # Set params for API requests
    def api_get_requests(self):
        params = {"start_date": "2021-07-31",
                "end_date": "2021-07-31",
                "api_key":NASDAQ_DATA_API_KEY
                }

# Do requests into API NASDAQ using params
        data = requests.get(f'https://data.nasdaq.com/api/v3/datasets/ECONOMIST/BIGMAC_{self.country}', params=params)
        return data.json()

class CreateS3Client:
    # Creating the low level functional client to connect with AWS S3.
    def create_s3_client(self):
        s3_client = boto3.client(
            's3',
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
            region_name='eu-central-1'
        )
        return  s3_client


class PutObjectFromApiToS3(CreateS3Client, RequestsBigMacIndexApi):

    def __init__(self, country, bucket, file_name):
        super().__init__(country)
        self.bucket = bucket
        self.file_name = file_name

    def s3_put_object(self):
        self.response = self.create_s3_client().put_object(
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
        self.s3_put_object()
        self.check_status_process()


class DeleteObjectFromS3(CreateS3Client):

    def __init__(self, bucket, file_name):
        self.bucket = bucket
        self.file_name = file_name

    def s3_delete_object(self):
        self.response = self.create_s3_client().delete_object(
            Bucket=self.bucket,
            Key=self.file_name,
            )

    def check_status_process(self):
        status = self.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status == 204:
            print(f"Successful S3 delete_object response. Status - {status}")
        else:
            print(f"Unsuccessful S3 delete_object response. Status - {status}")

    def run(self):
        self.s3_delete_object()
        self.check_status_process()


class GetListOfObjectInBucketS3(CreateS3Client):
    def __init__(self, bucket):
        self.bucket = bucket

    def get_objects_list_from_s3(self):
        self.response = self.create_s3_client().list_objects(
            Bucket= self.bucket
        )

        list_of_objects = [object['Key'] for object in self.response['Contents']]
        print(list_of_objects)

    def check_status_process(self):
        status = self.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status == 200:
            print(f"Successful S3 get list of object response. Status - {status}")
        else:
            print(f"Unsuccessful S3 get list of object response. Status - {status}")

    def run(self):
        self.get_objects_list_from_s3()
        self.check_status_process()


if __name__ == "__main__":

    # country = "ARG"
    # s3put = PutObjectFromApiToS3(country, S3_AWS_BUCKET, file_name=f"api_big_mac_index_{country}.json")
    # s3put.run()

    # s3delete = DeleteObjectFromS3(S3_AWS_BUCKET, 'api_big_mac_index_GBR.json')
    # s3delete.run()

    s3objectslist = GetListOfObjectInBucketS3(S3_AWS_BUCKET)
    s3objectslist.run()


