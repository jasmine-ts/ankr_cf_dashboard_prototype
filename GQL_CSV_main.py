#!/usr/bin/env python3

import sys
import pandas as pd
from datetime import datetime, timedelta
import requests
import argparse

# from daily_queries import *

# the endpoint of GraphQL API
url = 'https://api.cloudflare.com/client/v4/graphql/'

file_dir = '/Users/jasminetong-seely/Desktop/Ankr/dashboard_backend/24H_CSVs/'  # Must include trailing slash. If left blank,
# csv will be created in the current directory.
api_token = 'lL3Nzy3dgx1QvIhxECtEPhBeJEMGLMgYf_KNMRFo'
api_account = '873d1231a8a9343fb1203975dfa7d36d'
zone = 'd40d2e17bb61adcbe1842870bb3ce773'

# defining what arguments will be parsed and fed into main()
CLI=argparse.ArgumentParser()
CLI.add_argument("--offset_days", nargs=1, type=int, default=0)
CLI.add_argument("--historical_days", nargs=1, type=int, default=1)
CLI.add_argument("--dataset", nargs=1, type=str, default='')
CLI.add_argument("--raw_data_cols", nargs="*", type=str, default=[])
CLI.add_argument("--renamed_data_cols", nargs="*", type=str, default=[])
CLI.add_argument("--query_name", nargs=1, type=str, default='')
CLI.add_argument("--query_textfile", nargs=1, type=str, default='')
CLI.add_argument("--opt_filter", nargs=1, type=str, default='')
CLI.add_argument("--payload_flag", nargs=1, type=str, default='')

# Parse arguments and set GQL -> CSV pipeline in motion
def main():
    args = CLI.parse_args()

    offset_days = args.offset_days[0]
    historical_days = args.historical_days[0]
    dataset = args.dataset[0]
    raw_data_cols = args.raw_data_cols
    renamed_data_cols = args.renamed_data_cols
    query_name = args.query_name[0]
    query_textfile = args.query_textfile[0]
    opt_filter = args.opt_filter[0]
    payload_flag = args.payload_flag[0]

    start_date = get_past_date(offset_days + historical_days)
    end_date = get_past_date(offset_days)
 
    req = get_cf_graphql(start_date, end_date, query_textfile, opt_filter, payload_flag)
    if req.status_code == 200:
        print(req.status_code)
        convert_to_csv(req.text, start_date, end_date, dataset, raw_data_cols, renamed_data_cols, query_name)
    else:
        print("Failed to retrieve data: GraphQL API responded with {} status code".format(req.status_code))


# Get date variables in correct format
def get_past_date(num_days):
    today = datetime.utcnow().date()
    return today - timedelta(days=num_days)


# Send graphQL query, receive JSON response body for parsing
def get_cf_graphql(start_date, end_date, query_textfile, opt_filter, payload_flag):
    open_file = open(query_textfile, "r")
    query = open_file.read().replace('\n', '')

    assert(start_date <= end_date)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    # GQL query with no additional filter (date range only):
    payload_no_filter = f'''{{"query": "{query}",
        "variables": {{
          "zoneTag": "{zone}",
          "filter": {{
            "AND":[
                {{ "date_geq": "{start_date}" }},
                {{ "date_leq": "{end_date}" }}
            ]
          }}
        }}
      }}'''

    # GQL query with country name filter:
    payload_country_filter = f'''{{"query": "{query}",
        "variables": {{
          "zoneTag": "{zone}",
          "filter": {{
            "AND":[
                {{ "date_geq": "{start_date}" }},
                {{ "date_leq": "{end_date}" }},
                {{ "clientCountryName_like": "{opt_filter}" }}
            ]
          }}
        }}
      }}'''

    # GQL query with blockchain filter:
    payload_blockchain_filter = f'''{{"query": "{query}",
        "variables": {{
          "zoneTag": "{zone}",
          "filter": {{
            "AND":[
                {{ "date_geq": "{start_date}" }},
                {{ "date_leq": "{end_date}" }},
                {{ "clientRequestPath_like": "{opt_filter}" }}
            ]
          }}
        }}
      }}'''

    # Pick the correct payload variable based on input argument payload_flag
    if payload_flag == "no_filter":
      payload = payload_no_filter
    elif payload_flag == "country_filter":
      payload = payload_country_filter
    elif payload_flag == "blockchain_filter":
      payload = payload_blockchain_filter

    
    # Send the GraphQL query to Cloudflare; receive JSON response and return it
    r = requests.post(url, data=payload.replace('\n', ''), headers=headers)
    return r

# Parse and pipe JSON response into a CSV file
def convert_to_csv(raw_data, start_date, end_date, dataset, raw_data_cols, renamed_data_cols, query_name):
    data = pd.read_json(raw_data, dtype=False)['data']
    errors = pd.read_json(raw_data, dtype=False)['errors']

    # Check if we got any errors
    if errors.notna().any() or not 'viewer' in data or not 'zones' in data['viewer']:
        print(errors[0])
        print('Failed to retrieve data: GraphQL API responded with error:')
        return

    # Flatten nested JSON data first
    normalized_data = pd.json_normalize(data['viewer']['zones'], dataset)

    if len(normalized_data) == 0:
        print('We got empty response')
        return

    abridged_data = normalized_data[raw_data_cols]
    # Rename the columns to get friendly names
    abridged_data.columns = renamed_data_cols
      
    file = "{}{}-{}-{}.csv".format(file_dir, query_name, start_date, end_date)
    abridged_data.to_csv(file)
    print("Successfully exported to {}".format(file))


if __name__ == "__main__":
    main()