import os
import random
from time import sleep
from json import dumps
import json
import requests
import sys

gameID=sys.argv[1]
#578080 is PUBG: BATTLEGROUNDS (and has mixed reviews)
#489830 is Skyrim
#752580 is Imperium III HD

steam="https://store.steampowered.com/appreviews/"+str(gameID)
#10?json=1&cursor=AoIIPwYYanDTv%2BQB

f = open("./.dataset/new_dataset.txt", "w+")


limit=10000
if(len(sys.argv)>=3):
    limit=int(sys.argv[2])
    print("Limit is " + str(limit))
check=500
c0=0
c1=0
f.write('[')
def next_batch(cursor=None):
    global c0, c1, check, limit, f
    if(cursor is None):
        reviews = requests.get(steam, params={'json': '1', 'num_per_page' : 100, 'language' : 'all','day_range' : 9223372036854775807,'review_type' : 'all','purchase_type' : 'all'}, timeout=301)
    else:
        reviews = requests.get(steam, params={'json': '1', 'num_per_page' : 100, 'language' : 'all','day_range' : 9223372036854775807,'review_type' : 'all','purchase_type' : 'all', 'cursor':cursor}, timeout=301)
    if not (reviews is None):
        if not (reviews.content is None):
            #print(reviews.content)
            initial_json=json.loads(reviews.content)
            next_cursor = initial_json['cursor']
            data = initial_json['reviews']
            for review in data:
                c0=c0+1
                r_id = review['recommendationid']
                text = review['review'].replace('"','').replace('\n','').replace('\r','').replace('\t','').replace('\\','')
                positive = review['voted_up']
                p='0'
                if positive == True:
                    p='1'
                processed_review='{"id":'+r_id+',"text":"' + text + '","positive":' + p + '},\n'
                #write to file
                f.write(processed_review)
                #print(processed_review)
            print(next_cursor)
            if(c0>check):
                c0=c0-check
                c1=c1+check
                print(c1)
            if not (next_cursor is None) and (cursor!=next_cursor) and (c0+c1<limit):
                #sleep(1)
                next_batch(next_cursor)
            else:
                print("Finished with "+ str(c0+c1)+" reviews.")
        else:
            print("No content :(")
    else:
        print("No answer :(")


next_batch()

f.truncate(f.tell() - 2)
f.seek(0,2)
f.write(']')
f.close()

