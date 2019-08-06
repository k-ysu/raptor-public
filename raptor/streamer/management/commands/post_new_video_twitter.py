# -*- coding:utf-8 -*-


#Import models
from django.core.management.base import BaseCommand
from django.db import connection
from ...models import Youtube_Video
from ...models import Twitter_Post_History
from ...models import Game
from ...utility.twitter_client import TwitterClient
from ...utility.util import getRecommendVideos, getGameidFromStr
import random

import warnings
import sys


#import modules
import pprint
import datetime


class Command(BaseCommand):
    help = '--game_name [game_name_sys] : will tweet game new video, popular videos'
    help = '--post_type [1,2] : 1=>new video, 2=> popular video'

    twitter_conf = {
        'fortnite' : {
            'TWITTER_ACCOUNT' : 'CoreGameTV_fort',
            'CONSUMER_KEY' : 'XZqtnFkrxjzV3AwW2JZWeVzmy',
            'CONSUMER_SECRET' : 'um0krV0JsohiPUHZhwHumGgpUT3FK0C4d3B6XC9A0WgW7Ue3nQ',
            'ACCESS_KEY' : '1142106761660289029-OB3jSJrIxRCoSXJsI7uEZbVCllRHPh',
            'ACCESS_SECRET' : 'vjUyhOjNrz3i2mqcq9o3oA0Qi29iS3uUaWbJnRwxGJw1X',
        },
        'minecraft' : {
            'TWITTER_ACCOUNT' : 'CoreGameTV_mine',
            'CONSUMER_KEY' : 'DU0w02sr9TorEuTqxEotVvOzh',
            'CONSUMER_SECRET' : 'LBoyeONrTW1u1GhDmuLnRAoG9p67miFdwIf7ZOuI8v1bv9dGHn',
            'ACCESS_KEY' : '1150213621005217792-PJ8CaFSrkFNZr5kE95M0tQArKCIhiu',
            'ACCESS_SECRET' : 'Pv5jGhxvKgZw9wyUAqNkRQcN03AcBuOpF5TCZudhfgDwZ',
        },
        'knives-out' : {
            'TWITTER_ACCOUNT' : 'CoreGameTV_koya',
            'CONSUMER_KEY' : 'BSxixjVastURmi56rt7lXAhKg',
            'CONSUMER_SECRET' : 'zSrZQMAwb02j25tFjcXDu5vt1qztPXmPvo4uZphfl4Ufa5DuQ9',
            'ACCESS_KEY' : '1150263189952585728-U3g1AZQC5KaFu8nGQXymOwxYVU7x6F',
            'ACCESS_SECRET' : 'VtiQfJCQoa2DD8gsOSESqvoJUOz1Ral072eO80WiQEJ0p',
        },
        'super_mario_maker_2' : {
            'TWITTER_ACCOUNT' : 'CoreGame_mario',
            'CONSUMER_KEY' : 'YgAeSgShgHMqNToLurAGV6OqB',
            'CONSUMER_SECRET' : 'CQDWUfyAJFU4DeXlPT6z2d9VQW33OC8syceWBANI70aIn3UExH',
            'ACCESS_KEY' : '1158106375387398144-XK7YNILTDHlMNO7sKE5zAmykGUyR0k',
            'ACCESS_SECRET' : 'L8nEdA4HLDSk3zV6lzN1oSoXm2Uk3RBou0mfMvsHGUgX3',
        },
    }


    def add_arguments(self, parser):
            parser.add_argument('--game_name', required=True)
            parser.add_argument('--post_type' , required=True , help = '--post_type [1,2] : 1=>new video, 2=> popular video' )


    def handle(self, *args, **options):

        #Filter
        #warnings.filterwarnings("ignore", category=RuntimeWarning)

        dt_now = datetime.datetime.now()
        print("=======start get user from twitter : {}==========".format(dt_now))

        #Get game
        game_name = options['game_name']
        post_type = int(options['post_type'])
        games = Game.objects.filter(game_name_sys=game_name)
        game = None

        #Is Game Exist?
        if len(games)!=0:
            game = games[0]
            print("Sart Tweet About : {} ".format(game.game_name))
        else:
            print("Invalid Game Name")
            exit()

        done_tweet = False
        if post_type == 1:
            print("Post Type : New Video" )
            done_tweet = self.postNewVideo(game)
        elif post_type == 2:
            print("Post Type : Recommend Video" )
            done_tweet = self.postPopularVideo(game)
        else:
            print("Invalid Post Type")
            exit()


        print("===Post Tweet? : {} ===".format(done_tweet))
        print("=======END get user from twitter : {}==========".format(dt_now))

    def postPopularVideo(self,game):

        random_number = random.randint(1,32)
        if random_number != 1:
            print("Skip this time : {}".format(random_number))
            return False

        videos = getRecommendVideos(None,game.id,500)

        for v in videos:

            #Check title
            game_id_from_title = getGameidFromStr(v.video_title)
            if game.id != game_id_from_title:
                continue

            #Check table if it is tweeted.
            isPost = self.checkPost(v.youtube_video_id, game)
            if isPost:
                continue

            #Post Tweet
            done_tweet = self.tweetPopularVideo(v, game)

            #Break if post tweeted
            break

        return done_tweet



    def postNewVideo(self,game):

        #Search Videos last 24h
        where_sql = "active = 1 and is_ready = 1 and game_id = {} and  date(youtube_created_at)   >= date(now()) - INTERVAL 24 HOUR ".format(game.id)
        videos = Youtube_Video.objects.extra(where=[ where_sql ]).order_by('-youtube_created_at')

        #Tweet once per process ( process run every 15min )
        done_tweet = False
        for v in videos:

            #Check title
            game_id_from_title = getGameidFromStr(v.video_title)
            if game.id != game_id_from_title:
                continue


            #Check table if it is tweeted.
            isPost = self.checkPost(v.id, game)
            if isPost:
                continue

            #Post Tweet
            done_tweet = self.tweetNewVideo(v, game)

            #Break if post tweeted
            break

        return done_tweet


    def checkPost(self,video_id,game):

        twitter_conf = self.twitter_conf[game.game_name_sys]
        url = "https://coregame.jp/video/{}".format(video_id)
        results = Twitter_Post_History.objects.filter(url = url, twitter_account = twitter_conf["TWITTER_ACCOUNT"])
        if len(results) > 0:
            return True
        else:
            return False


    def getTwitterClient(self,game):

        twitter_conf = self.twitter_conf[game.game_name_sys]
        twitter_api = TwitterClient()

        #Set Twitter Keys, initilize
        twitter_api.setConsumerKey(twitter_conf["CONSUMER_KEY"])
        twitter_api.setConsumerSecret(twitter_conf["CONSUMER_SECRET"])
        twitter_api.setAccessKey(twitter_conf["ACCESS_KEY"])
        twitter_api.setAccessSecret(twitter_conf["ACCESS_SECRET"])
        twitter_api.initializeApiClient()

        return twitter_api

    def tweetPopularVideo(self,video,game):

        #tweet message
        message = "本日の #{} おすすめ動画！最近の中でもっとも高評価を得た動画です！\n"
        message = message.format(game.game_name_jp)

        #Streamer
        streamer = video.streamer
        message = message + "ゲーム実況者 : {}".format(streamer.streamer_name)
        if streamer.twitter_id is not None:
            message = message + "(@{})"
            message = message.format(streamer.twitter_id)
        message = message + "\n"

        #Video Title
        title = video.video_title
        if len(title)>25:
            title = title[0:25] + "..."
        message = message + title + "\n\n\n\n"

        #URL
        post_url = "https://coregame.jp/video/{}".format(video.youtube_video_id)
        message = message + "↓コアゲームTVで最新,おすすめの{}の動画チェック↓\n".format(game.game_name_jp)
        message = message + post_url

        done_tweet = self.postMessage(message,post_url,game)
        return done_tweet

    def tweetNewVideo(self,video,game):


        #tweet message
        message = "#{} の新着動画！\n"
        message = message.format(game.game_name_jp)

        #Streamer
        streamer = video.streamer
        message = message + "ゲーム実況者 : {}".format(streamer.streamer_name)
        if streamer.twitter_id is not None:
            message = message + "(@{})"
            message = message.format(streamer.twitter_id)
        message = message + "\n"

        #Video Title
        title = video.video_title
        if len(title)>40:
            title = title[0:40] + "..."
        message = message + title + "\n\n\n\n"

        #URL
        post_url = "https://coregame.jp/video/{}".format(video.id)
        message = message + "↓コアゲームTVで最新の{}の動画チェック↓\n".format(game.game_name_jp)
        message = message + post_url

        done_tweet = self.postMessage(message,post_url,game)
        return done_tweet

    def postMessage(self,message,post_url,game):

        #Twitter Client
        twitter_conf = self.twitter_conf[game.game_name_sys]
        twitter_api = self.getTwitterClient(game)

        try:

            # Post Message
            print("====Post Message===")
            print(message)
            twitter_api.postTweet(message)

            #Record History
            history = Twitter_Post_History()
            history.url = post_url
            history.twitter_account = twitter_conf["TWITTER_ACCOUNT"]
            history.save()
            return True


        except Exception as e:

            print('=======================ERROR START=======================')
            dt_error_now = datetime.datetime.now()
            print('{} : Twitter URL => {} '.format(dt_error_now,post_url))
            tb = sys.exc_info()[2]
            print("message:{0}".format(e.with_traceback(tb)))
            print('=======================ERROR END=======================')
            return False
