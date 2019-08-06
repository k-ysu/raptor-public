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

    def handle(self, *args, **options):

            dt_now = datetime.datetime.now()
            print("=======start register_popular_video : {}==========".format(dt_now))

            stream_id = options['streamer_id']

            #list of streamer objects
            streamers = []

            #get all objects
            if stream_id is None:
                streamers = Streamer.objects.extra(where=[ "will_update_popular_video = 1"]);

            #get single objecct
            else:
                streamers = Streamer.objects.extra(where=[ "id = {}".format(stream_id) ])

            #Update Streamers Data
            for s in streamers:

                print("Regist New Vifro from : {}".format(s.streamer_name))

                if s.youtube_upload_list_id is not None:

                    yapi = YoutubeApi()
                    yapi.registerPopularVideo(s)

                #set streamer flag to False
                s.will_update_popular_video = False
                s.save()
