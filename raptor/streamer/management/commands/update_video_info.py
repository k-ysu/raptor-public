# -*- coding:utf-8 -*-


#Import models
from django.core.management.base import BaseCommand
from ...models import Youtube_Video

#import modules
from ...utility.youtube_api import YoutubeApi
import pprint
import datetime



class Command(BaseCommand):




    def add_arguments(self, parser):
            parser.add_argument('--youtube_video_id' , help = '--youtube_video_id [id] : update or create specific video info ')
            parser.add_argument('--video_search' , required=True , help = '--video_search [1,2,3] : 1=>all, 2=>Recent video(4days), 3=>will update only , 5=> id%10 = day(now())%1  , 4=>specific video' )
            parser.add_argument('--info_type' ,  required=True , help = '--info_type [1,2] : 1=>all, 2=>static')
            parser.add_argument('--exec', action='store_true' , help = 'no update without this')


    def handle(self, *args, **options):

            dt_now = datetime.datetime.now()
            print("=======start video info : {}==========".format(dt_now))

            youtube_video_id = options['youtube_video_id']
            video_search = int(options['video_search'])
            info_type = int(options['info_type'])
            exec_type = int(options['exec'])


            print("Search Type =>{} , Info Type => {}".format(video_search,info_type))

            #list of streamer objects
            videos = []
            where_state = ""
            info_all = False
            execution_true=False
            update_type = ""

            if info_type == 1:
                info_all = True

            if exec_type == 1:
                execution_true = True


            #print(info_all)

            if youtube_video_id is not None:
                where_state = "id = '{}'".format(youtube_video_id)
                update_type = "SPECIFIC"
            elif video_search == 1:
                where_state =  " active = True AND is_low_views=0 "
                update_type = "ALL"
            elif video_search == 2:

                where_state = " DATEDIFF(current_date,youtube_created_at) <= 4  AND is_low_views=0 AND  "
                where_state += " active = True "
                update_type = "RECENT UPLOAD(last 4days)"

            elif video_search == 3:
                 where_state = " will_info_update = 1 AND active = True  AND is_low_views=0"
                 update_type = "WILL INFO UPDATE ONLY"
            elif video_search == 4:
                 where_state = " mod(id,10) =  mod(day(now()),10) AND active = True AND is_low_views=0 "
                 #where_state = " id =  1 AND active = True  "
                 update_type = "ONCE EVERY 10DAYS"
            else:
                print("invalid video search type => exit")
                exit()

            #print(where_state)
            videos = Youtube_Video.objects.extra(where=[ "{}".format(where_state) ]);
            #exec_sql = "SELECT * FROM streamer_youtube_video WHERE " + where_state
            #videos = Youtube_Video.objects.raw(exec_sql)

            print(" Update Type => {}, Will update {} videos, all info update => {}".format(update_type,len(videos),info_all))
            print(" EXEC MODE => {}".format(execution_true))

            if execution_true == False:
                print("No Exec Mode. Exit here. please add --exec for update ")
                return;

            #Update Videos Data
            YVideos = {}
            video_ids = ''
            yapi = YoutubeApi()

            for v in videos:

                #print("video_id:{},youtube_video_org_id:{}".format(v.id, v.youtube_video_org_id))

                YVideos['{}'.format(v.youtube_video_org_id)] = v
                video_ids += v.youtube_video_org_id
                video_ids += ','
                if len(YVideos) == 50:

                    #Update Video Info
                    yapi.updateVideoInfo(YVideos,video_ids,info_all)

                    #Initializes
                    YVideos = {}
                    video_ids =''


            #Update the rest of videos
            if len(YVideos) > 0:
                fake = '123'
                yapi.updateVideoInfo(YVideos,video_ids,info_all)
