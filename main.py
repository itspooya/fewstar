import tweepy
import json
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import time
MONGO_HOST = 'mongodb://Usename:Password@Server:Port/?authSource=databasecontainingauth'
while(True):
    with open("twitter_creds.json") as f:
                config = json.load(f)
    consumer_key = config["consumer_token"]
    consumer_secret = config["consumer_secret"]
    access_token = config["access_token"]
    access_token_secret = config["access_secret"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    messages_to_send = []
    client = MongoClient(MONGO_HOST)
    db = client.DBNAME
    count = db.Collectionname.count_documents({})
    mylist = []
    print(count)
    for tweet_id in db.Collectionname.find():
        mylist.append(tweet_id['id'])
    for tweet in tweepy.Cursor(api.search, q="min_faves:1000 lang:fa", tweet_mode='extended',count=100).items(100):
        if tweet.id in mylist:
            continue
        else:
            messages_to_send.append(tweet)
    for item in messages_to_send:
        try:
             db.Collectionname.insert_one({'id':item.id})
        except DuplicateKeyError as e:
             continue
    for item in messages_to_send:
        api.retweet(id=item.id)
    print("Sleeping")
    time.sleep(900)