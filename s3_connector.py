import boto3
import json
import requests
from decouple import config


NASDAQ_DATA_API_KEY = config("NASDAQ_DATA_API_KEY")
S3_AWS_BUCKET = config("S3_AWS_BUCKET")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")


def get_big_mac_idex_json(country="ROU", **kwargs):
    params = {"start_date": "2021-07-31",
            "end_date": "2021-07-31",
            "api_key":NASDAQ_DATA_API_KEY
            }
    if kwargs:
        params.update(**kwargs)

    data = requests.get(f'https://data.nasdaq.com/api/v3/datasets/ECONOMIST/BIGMAC_{country}', params=params)
    return data.json()


class S3Connector:
    def __init__(self):
        self._client = self._create_s3()

    def _create_s3(self):
        s3_client = boto3.client(
            's3',
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
            region_name='eu-central-1'
        )
        return  s3_client

    def put(self, bucket:str, file_name:str, file):
        self._client.put_object(
            Bucket=bucket,
            Key=file_name,
            Body=json.dumps(file)
        )
        print(f"{file_name} was putted correctly into bucket.")

    def delete(self, bucket:str, file_name:str):
        self._client.delete_object(
            Bucket=bucket,
            Key=file_name,
            )
        print(f"{file_name} was deleted correctly from bucket.")

    def take_list_of_objects_in_bucket(self, bucket:str):
            response = self._client.list_objects(
                Bucket=bucket
            )
            try:
                list_of_objects = [object['Key'] for object in response['Contents']]
            except TypeError:
                list_of_objects = []
            print(list_of_objects)

if __name__ == "__main__":
    data = get_big_mac_idex_json()
    s3connector = S3Connector()
    # s3connector.put(S3_AWS_BUCKET, 'bic_mac_index_ROU.json', data)
    s3connector.delete(S3_AWS_BUCKET, 'bic_mac_index_ROU.json')


