import tweepy
import json
import telegram
import time
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
    with open("sinceid.json") as myf:
        c2 = json.load(myf)
    file_since_id = c2["sinceid"]
    max_id = 0
    messages_to_send = []
    for tweet in tweepy.Cursor(api.search, q="min_faves:1000 lang:fa", tweet_mode='extended',since_id=file_since_id).items():
        if max_id<tweet.id:
            max_id = tweet.id
        messages_to_send.append(tweet)
    with open('sinceid.json',"w") as up:
        if max_id<file_since_id:
            max_id=file_since_id
        up.write("""{"sinceid":%s}"""%max_id)
    
    bot = telegram.Bot(token="")
    
    for item in messages_to_send:
        if 'media' in item.entities:
            if item.entities['media'][0]['type']=="photo":
                for image in  item.entities['media']:
                    bot.send_photo(chat_id="@channelname",photo=image['media_url'],caption=item.full_text+"\n https://twitter.com/{}/status/{}".format(item.user.screen_name,item.id))
            elif(item.entities['media'][0]['type']=="video"):
                for video in item.entities['media']:
                    bot.sendVideo(chat_id="@channelname",video=video['media_url'],caption=item.full_text+"\n https://twitter.com/{}/status/{}".format(item.user.screen_name,item.id))
        else:
            bot.send_message(chat_id="@channelname",text=item.full_text+"\n https://twitter.com/{}/status/{}".format(item.user.screen_name,item.id))
    time.sleep(3*60*60)
