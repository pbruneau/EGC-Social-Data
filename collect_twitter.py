import tweepy
import codecs
import json
from pprint import pprint

#Twitter API credentials, have to be obtained from https://apps.twitter.com/
consumer_key = "CONSUMER_KEY"
consumer_secret = "CONSUMER_SECRET"
access_key = "ACCESS_KEY"
access_secret = "ACCESS_SECRET"


# Note1: the tweet of a given user is a retweet if retweeted_status exists.
# Note2: https://developer.twitter.com/en/developer-terms/agreement-and-policy.html#f-be-a-good-partner-to-twitter

def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
	# write tweets as JSON array
    outfile = codecs.open('{}'.format('EGC_tweets.json'), 'w', encoding="utf-8")
    outfile.write('[')
    
    # initialize a list to hold all the tweepy Tweets
    alltweets = []
    
    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    # save most recent tweets
    alltweets.extend(new_tweets)
    
    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    original_cnt = 0
    retweet_cnt = 0
    like_cnt = 0
    
    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        # save most recent tweets
        alltweets.extend(new_tweets)
        
        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

    for tweet in alltweets:
        tweet = tweet._json
        json.dump(tweet, outfile, ensure_ascii=False, indent=2)
        outfile.write(',')
        if 'retweeted_status' not in tweet:
            original_cnt += 1
            retweet_cnt += tweet['retweet_count']
            like_cnt += tweet['favorite_count']
    
    outfile.write(']')
    print('downloaded %d tweets' % (len(alltweets)))
    print('original tweets: %d' % (original_cnt))
    print('retweets: %d' % (retweet_cnt))
    print('likes: %d' % (like_cnt))
    
get_all_tweets("associationEGC")
