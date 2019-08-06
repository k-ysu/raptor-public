import tweepy


class TwitterClient():

    #Channel API detail ( now using esports.raptor@gmail.com account)
    CONSUMER_KEY = None #keep the quotes, replace this with your consumer key
    CONSUMER_SECRET = None  #keep the quotes, replace this with your consumer secret key
    ACCESS_KEY = None #keep the quotes, replace this with your access token
    ACCESS_SECRET = None #keep the quotes, replace thbis with your access token secret
    twitter_api = None

    #api
    api = None

    #def __init__(self):
        #auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        #auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
        #self.api = tweepy.API(auth)

    def setConsumerKey(self , str):
        self.CONSUMER_KEY = str

    def setConsumerSecret(self , str):
        self.CONSUMER_SECRET = str

    def setAccessKey(self , str):
        self.ACCESS_KEY = str

    def setAccessSecret(self , str):
        self.ACCESS_SECRET = str

    def initializeApiClient(self):
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
        self.api = tweepy.API(auth)

    def postTweet(self, str):
        self.api.update_status(str)



    #def UpdateStreamerInfo(self , s):

        #user = self.api.get_user(s.twitter_id)
        #followersCount = user.followers_count
        #followingCount = user.friends_count

        #update streamer infor
        #s.twitter_followers = followersCount
        #s.twitter_followings = followingCount
        #s.save()
