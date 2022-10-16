import os
import random
from time import sleep
from json import dumps
from kafka import KafkaProducer


#https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a
#https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Filtered-Stream/filtered_stream.py
# For sending GET requests from the API
import requests
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
#import time
from datetime import datetime

#print(datetime.now().isoformat(timespec='seconds'))

#tap_pyToLogstash
topic = os.getenv("KAFKA_TOPIC", "tap_pyToLogstash")
producer = KafkaProducer(bootstrap_servers=['kafkaServer:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


f = open("TWITTER_CREDENTIALS.txt", 'r')

#api_key=f.readline().strip('\n\r')
#api_secret=f.readline().strip('\n\r')
bearer_token=f.readline().strip('\n\r')
#access_token=f.readline().strip('\n\r')
#access_secret=f.readline().strip('\n\r')

f.close()

def bearer_oauth(r):

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "TAPv2SampledStreamPython"
    return r

def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    #print(json.dumps(response.json()))

def set_rules():
    delete_all_rules(get_rules())
    f1 = open("TWITTER_KEYWORD.txt", 'r')
    key=f1.readline().strip('\n\r')
    sample_rules = [
        {"value": key, "tag": key}
    ]
    #sample_rules = [
    #    {"value": "Salvini EldenRing -has-mentions"},
    #    #{"value": "#EldenRing"},
    #]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    f1.close()

#sample_rules = [
#        {"value": "EldenRing"},
#    ]
#payload = {"add": sample_rules}


set_rules()
response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )


for response_line in response.iter_lines():
    if response_line:
        json_response = json.loads(response_line)
        print(json_response)
        #tmp=json_response['@timestamp']
        #tmp.replace("@","")
        json_id=json_response['data']['id']
        json_response= json_response['data']['text']
        final_json={
            "id": json_id,
            "text":json_response,
            "timestamp":datetime.now().isoformat(timespec='seconds')
        }
        #json_response= '{"'+ json_id +'":' + '"' + json_response + '"}'
        print(final_json)
        #print(json.dumps(json_response, indent=4, sort_keys=True))
        producer.send(topic, value=final_json)


