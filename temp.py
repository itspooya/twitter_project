import tweepy
import json
import telegram
import time
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import re
MONGO_HOST = 'mongodb://localhost/databasename'

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
    client = MongoClient()
    db = client.databasename
    count = db.document.count_documents({})
    mylist = []
    print(count)
    for tweet_id in db.collectionname.find():
        mylist.append(tweet_id['id'])
    for tweet in tweepy.Cursor(api.search, q="min_faves:1000 lang:fa", tweet_mode='extended',count=100).items(100):
        if tweet.id in mylist:
            continue
        else:
            messages_to_send.append(tweet)
    for item in messages_to_send:
        try:
             db.collectionname.insert_one({'id':item.id})
        except DuplicateKeyError as e:
             continue
    bot = telegram.Bot(token="")
    for item in messages_to_send:
        try:
            if 'media' in item.extended_entities:
                if item.extended_entities['media'][0]['type']=="photo":
                    for image in  item.extended_entities['media']:
                        try:
                            bot.send_photo(chat_id="@channelname",photo=image['media_url'],caption=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
                            time.sleep(5)
                        except telegram.error.BadRequest:
                            bot.send_video(chat_id="@channelname",video=image['video_info']['variants'][0]['url'],caption=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
                            time.sleep(5)
                elif(item.extended_entities['media'][0]['type']=="video"):
                    for video in item.extended_entities['media']:
                        try:
                            bot.send_video(chat_id="@channelname",video=video['video_info']['variants'][0]['url'],caption=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
                            time.sleep(5)
                        except telegram.error.BadRequest:
                            try:
                                bot.send_video(chat_id="@channelname",video=video['video_info']['variants'][1]['url'],caption=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
                                time.sleep(5)
                            except telegram.error.BadRequest:
                                bot.send_photo(chat_id="@channelname",photo=video['media_url'],caption=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
                                time.sleep(5)
            else:
                bot.send_message(chat_id="@channelname",text=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
        except(AttributeError):
            if 'media' in item.entities:
                if item.entities['media'][0]['type']=="photo":
                    for image in  item.entities['media']:
                        try:
                            bot.send_photo(chat_id="@channelname",photo=image['media_url'],caption=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
                            time.sleep(5)
                        except telegram.error.BadRequest:
                            bot.send_video(chat_id="@channelname",video=image['video_info']['variants'][0]['url'],caption=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
                            time.sleep(5)
                elif(item.entities['media'][0]['type']=="video"):
                    for video in item.entities['media']:
                        try:
                            bot.send_video(chat_id="@channelname",video=video['video_info']['variants'][0]['url'],caption=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
                            time.sleep(5)
                        except telegram.error.BadRequest:
                            try:
                                bot.send_video(chat_id="@channelname",video=video['video_info']['variants'][1]['url'],caption=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
                                time.sleep(5)
                            except telegram.error.BadRequest:
                                bot.send_photo(chat_id="@channelname",photo=video['media_url'],caption=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
                                time.sleep(5)
            else:
                bot.send_message(chat_id="@channelname",text=re.sub(r"http\S+","",item.full_text)+'\n <a href="https://twitter.com/{}/status/{}">{}</a>'.format(item.user.screen_name,item.id,item.user.name),parse_mode=telegram.ParseMode.HTML,disable_web_page_preview=True)
    time.sleep(900)
