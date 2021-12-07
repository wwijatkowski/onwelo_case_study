import boto3
import json
import requests
from decouple import config

NASDAQ_DATA_API_KEY = config("NASDAQ_DATA_API_KEY")
S3_AWS_BUCKET = config("S3_AWS_BUCKET")
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")


# Creating the low level functional client to connect with AWS S3.
s3_client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name='eu-central-1'
    )

#Set params for requests
params = {"start_date": "2021-07-31",
          "end_date": "2021-07-31",
          "api_key":NASDAQ_DATA_API_KEY
          }

# Set country code from file "economist_country_codes.csv"
country = "POL"

# Do requests into API NASDAQ using params
data = requests.get(f'https://data.nasdaq.com/api/v3/datasets/ECONOMIST/BIGMAC_{country}', params=params)
data_json = data.json()


# Change to json file and save into local dictionary
with open(f'bic_mac_index_{country}.json', 'w') as f:
    json.dump(data_json, f)

# Put object(created json file) to AWS S3
response = s3_client.put_object(
    Bucket=S3_AWS_BUCKET,
    Key=f'bic-mac-index-{country}.json',
    Body=json.dumps(data_json)
    )

status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
if status == 200:
    print(f"Successful S3 put_object response. Status - {status}")
else:
    print(f"Unsuccessful S3 put_object response. Status - {status}")