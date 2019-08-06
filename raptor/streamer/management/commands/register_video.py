# -*- coding:utf-8 -*-


#Import models
from django.core.management.base import BaseCommand
from ...models import Streamer
from ...models import Youtube_Video

#import modules
from ...utility.youtube_api import YoutubeApi
from ...utility.twitter_api import TwitterApi
import pprint
import datetime



class Command(BaseCommand):
    help = '--streamer_id [id] : update specific streamer info'

    def add_arguments(self, parser):
            parser.add_argument('--streamer_id')
            parser.add_argument('--all', action='store_true')
            parser.add_argument('--new_streamer', action='store_true')
            parser.add_argument('--is_all_videos', action='store_true')

    def handle(self, *args, **options):

            dt_now = datetime.datetime.now()
            print("=======start register_video : {}==========".format(dt_now))

            stream_id = options['streamer_id']
            is_all = options['all']
            is_all_videos = options['is_all_videos']
            new_streamer = options['new_streamer']


            #list of streamer objects
            streamers = []

            #get all objects
            if is_all is True:
                streamers = Streamer.objects.all();
                print("Regist New Videos from all streamer")
            elif new_streamer is True:
                streamers = Streamer.objects.extra(where=[ " will_update_popular_video = 1 "  ])
                print("Regist ALL Videos from new streamer")
            elif stream_id is not None:
                streamers = Streamer.objects.extra(where=[ "id = {}".format(stream_id) ])
                print("Regist New videos from specfic streamer ")
            else:
                where_sql = "  date(last_youtube_uploaded) >= date(now()) - INTERVAL 2 day  "
                streamers = Streamer.objects.extra(where=[ where_sql ])
                print("Regist New videos from specfic streamer ")

            #Update Streamers Data
            for s in streamers:

                print("Regist New Vifro from : {}".format(s.streamer_name))

                if s.youtube_upload_list_id is not None:

                    #pprint.pprint(s)

                    yapi = YoutubeApi()
                    yapi.registerNewVideo(s,is_all_videos)

                    # Unflag
                    if new_streamer is True and is_all_videos is True:
                        s.will_update_popular_video = False
                        s.save()
