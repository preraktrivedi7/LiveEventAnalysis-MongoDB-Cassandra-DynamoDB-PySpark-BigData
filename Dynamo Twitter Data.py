from __future__ import print_function
import tweepy
import json
import requests
from dateutil import parser
import json


import boto3
import json


WORDS = ['#Adrian', '#Oblak']

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""


def store_dynamo_db(created_at, text, screen_name, tweet_id):


    ACCESS_KEY =""
    SECRET_KEY = ""
#    ACCESS_KEY =""
 #   SECRET_KEY = ""
#    session = boto3.Session(
 #   aws_access_key_id=ACCESS_KEY,
  #  aws_secret_access_key=SECRET_KEY,
   # )
 # ACCESS_KEY =""
   # SECRET_KEY = ""
    #SESSION_TOKEN = ""
   # dynamo = boto3.client(service_name='dynamodb', region_name='us-east-1')
    dynamo = boto3.resource('dynamodb',region_name='us-east-1')

    table = dynamo.Table('tweets')
#    s,sc = get_sentiment(text)
    from decimal import Decimal
    table.put_item(
    Item={
        "created_at":str(created_at),
        "screen_name":screen_name,
        "text":text,
        "tweet_id":str(tweet_id)
 #       "sentiment":s,
  #      "sentiment_score":Decimal(sc)
        }
    )

    print("Done")


class StreamListener(tweepy.StreamListener):
    #This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
 print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
           # Decode the JSON from Twitter
            datajson = json.loads(data)

            #grab the wanted data from the Tweet
            text = datajson['text']
            screen_name = datajson['user']['screen_name']
            tweet_id = datajson['id']
            created_at = parser.parse(datajson['created_at'])


            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))

            #insert the data into the MySQL database
            #store_data_cassandra(created_at, text, screen_name, tweet_id)

            #store_data_mongo(created_at, text, screen_name, tweet_id)
            store_dynamo_db(str(created_at), text, screen_name, tweet_id)
            #store_data_dynamo(created_at, text, screen_name, tweet_id)
 def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
           # Decode the JSON from Twitter
            datajson = json.loads(data)

            #grab the wanted data from the Tweet
            text = datajson['text']
            screen_name = datajson['user']['screen_name']
            tweet_id = datajson['id']
            created_at = parser.parse(datajson['created_at'])


            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))

            #insert the data into the MySQL database
            #store_data_cassandra(created_at, text, screen_name, tweet_id)

            #store_data_mongo(created_at, text, screen_name, tweet_id)
            store_dynamo_db(str(created_at), text, screen_name, tweet_id)
            #store_data_dynamo(created_at, text, screen_name, tweet_id)

        except Exception as e:
           print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)

