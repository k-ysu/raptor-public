import tweepy


class TwitterApi():

    #Channel API detail ( now using esports.raptor@gmail.com account)
    CONSUMER_KEY = 'fake'#keep the quotes, replace this with your consumer key
    CONSUMER_SECRET = 'fake' #keep the quotes, replace this with your consumer secret key
    ACCESS_KEY = 'fake'#keep the quotes, replace this with your access token
    ACCESS_SECRET = 'fake'#keep the quotes, replace thbis with your access token secret

    #api
    api = None

    def __init__(self):
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
        self.api = tweepy.API(auth)

    def UpdateStreamerInfo(self , s):

        user = self.api.get_user(s.twitter_id)
        followersCount = user.followers_count
        followingCount = user.friends_count

        #update streamer infor
        s.twitter_followers = followersCount
        s.twitter_followings = followingCount
        s.save()
