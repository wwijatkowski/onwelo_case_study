from decouple import config
import requests
import json
import csv


NASDAQ_DATA_API_KEY = config("NASDAQ_DATA_API_KEY")

#Set params for requests
params = {"start_date": "2021-07-31",
          "end_date": "2021-07-31",
          "api_key":NASDAQ_DATA_API_KEY,
          "column_index": 3
          }

###Create dict from csv file with Country: code.

countries_with_code_dict = {}
with open('../economist_country_codes.csv') as csv_file:
    csv_file = csv.DictReader(csv_file, delimiter="|")
    for row in csv_file:
        countries_with_code_dict[row["COUNTRY"]] = row["CODE"]

# Create json file of all countries with Big Mac index ---> country((full_contry_name): Big_Mac_index
all_countries_big_mac_index_dict = dict()
for country, code in countries_with_code_dict.items():
    data = requests.get(f'https://data.nasdaq.com/api/v3/datasets/ECONOMIST/BIGMAC_{code}/data.json', params=params)
    date_and_big_mac_index_list = data.json()['dataset_data'].get('data', None)
    if len(date_and_big_mac_index_list) == 1:
        all_countries_big_mac_index_dict[country] = round(date_and_big_mac_index_list[0][1], 2)
    else:
        continue
with open(f'bic_mac_index_all_countries.json', 'w') as f:
    json.dump(all_countries_big_mac_index_dict, f)


