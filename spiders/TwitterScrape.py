from datetime import datetime
from urllib.parse import urlparse

import tweepy
import configparser

from dateutil.relativedelta import relativedelta
from pytz import utc
import numpy as np
import pandas as pd


class TwiterScraper:

    def __init__(self, urls):
        self.urls = urls
        self.config = configparser.RawConfigParser()
        self.config.read('config.ini')
        self.api_key = self.config['twitter']['api_key']
        self.api_sec_key = self.config['twitter']['api_sec_key']
        self.acc_tok = self.config['twitter']['acc_tok']
        self.acc_sec_tok = self.config['twitter']['acc_sec_tok']
        self.bear_tok = self.config['twitter']['bear_tok']

    def send_usernames(self):
        with open('files/twitter.csv', 'w')as f:
            f.write("Twitter,followers_count,num_tweets,ret,rep,fav\n")
        for url in self.urls:
            list_all = []
            user_name = urlparse(url).path.split('/')[-1]
            list_tweets, followers_count = self.get_tweets(user_name)
            ret, rep, fav, num_tweets = self.get_tweets_replies(list_tweets)
            list_all.append([url, followers_count, num_tweets, ret, rep, fav])
            self.write(list_all)

    def get_tweets(self, username):
        self.auth = tweepy.OAuth1UserHandler(self.api_key, self.api_sec_key)
        self.auth.set_access_token(self.acc_tok, self.acc_sec_tok)
        api = tweepy.API(self.auth)
        try:
            tweets = api.user_timeline(screen_name=username)
            list_tweets = []
            for tweet in tweets:
                if tweet.created_at > (datetime.today() - relativedelta(month=3)).replace(tzinfo=utc):
                    list_tweets.append(tweet.id_str)
            user = api.get_user(screen_name =username)
            followers_count = user.followers_count
            return list_tweets, followers_count
        except:
            return "username doesn't exist", "username doesn't exist"

    def get_tweets_replies(self, list_tweets):
        self.client = tweepy.Client(bearer_token=self.bear_tok, consumer_key=self.api_key,
                consumer_secret=self.api_sec_key, access_token=self.acc_tok,
                access_token_secret=self.acc_sec_tok)
        if list_tweets == "username doesn't exist":
            return 0, 0, 0, 0
        if len(list_tweets) !=0:
            tweet = self.client.get_tweets(ids=list_tweets, tweet_fields=['public_metrics'])
            list_stats = []
            for stat in tweet.data:
                list_stats.append([stat.public_metrics['retweet_count'],
                                   stat.public_metrics['reply_count'], stat.public_metrics['like_count']])
            np_arr = np.sum(list_stats, axis=0)
            ret = np_arr[0]
            rep = np_arr[1]
            fav = np_arr[2]
            return ret, rep, fav, len(list_tweets)
        else:
            return 0, 0, 0, 0

    def write(self, list_all):
        df1 = pd.DataFrame(list_all)
        df1.to_csv('files/twitter.csv', index=False, mode='a',header=False)
