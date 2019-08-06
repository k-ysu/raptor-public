# -*- coding:utf-8 -*-


#Import models
from django.core.management.base import BaseCommand
from ...models import Streamer

#import modules
from ...utility.youtube_api import YoutubeApi
from ...utility.twitter_api import TwitterApi
import pprint
import datetime
import sys



class Command(BaseCommand):
    help = '--streamer_id [id] : update specific streamer info'
    help = '--greater_id [id] : update sreamer which is bigger than specified id'

    def add_arguments(self, parser):
            parser.add_argument('--streamer_id')
            parser.add_argument('--greater_id')
            parser.add_argument('--non_ready', action='store_true' , help = 'update for non-ready streamer')

    def handle(self, *args, **options):

            dt_now = datetime.datetime.now()
            print("=======start update_streamer_info : {}==========".format(dt_now))

            stream_id = options['streamer_id']
            greater_id = options['greater_id']
            non_ready = int(options['non_ready'])

            #list of streamer objects
            streamers = []

            #get all objects
            if stream_id is not None:
                streamers = Streamer.objects.extra(where=[ "id = {}".format(stream_id) ])
            elif greater_id is not None:
                streamers = Streamer.objects.extra(where=[ "id >= {}".format(greater_id) ])
            elif non_ready == 1:
                streamers = Streamer.objects.extra(where=[ " is_ready = 0 " ])
            else:
                streamers = Streamer.objects.all();


            #Update Streamers Data
            for s in streamers:

                print("Update : {}".format(s.streamer_name))

                #update streamer youtube info
                if s.youtube_channel_id is not None:
                    #print('skip youtube')
                    yapi = YoutubeApi()

                    try:

                        #print('skip youtube')
                        yapi.UpdateStreamerInfo(s)

                    except Exception as e:
                        print('=======================ERROR START : Update Streamer Info ( Youtube ) =======================')
                        dt_error_now = datetime.datetime.now()
                        print('{} : Streamer ID=> {}, Streamer Name => {} '.format(dt_error_now,s.id,s.streamer_name))
                        tb = sys.exc_info()[2]
                        print("message:{0}".format(e.with_traceback(tb)))
                        print('=======================ERROR END=======================')



                #updaste streamer twitter info
                if s.twitter_id is not None:

                    #print('skip twitter')
                    tapi = TwitterApi()

                    try:

                        #print('skip twitter')
                        tapi.UpdateStreamerInfo(s)

                    except Exception as e:
                        print('=======================ERROR START : Update Streamer Info ( Twitter ) =======================')
                        dt_error_now = datetime.datetime.now()
                        print('{} : Streamer ID=> {}, Streamer Name => {} '.format(dt_error_now,s.id,s.streamer_name))
                        tb = sys.exc_info()[2]
                        print("message:{0}".format(e.with_traceback(tb)))
                        print('=======================ERROR END=======================')
